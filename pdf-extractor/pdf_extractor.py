import csv
import requests
from bs4 import BeautifulSoup
import lxml
from downloader import start_download
from pdf2image import convert_from_path
from PIL import Image

import pytesseract
pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

import json
import os
import sys



def get_links_from_csv(csv_file):
    links = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            links.append(row[0])  
    return links


def download(pdf_link):
    return start_download(pdf_link, './downloaded_pdfs')[0]


def scrape_link(page_link):
    
    pdf_link = ""

    html = requests.get(page_link).text
    html = BeautifulSoup(html, "lxml")

    download_options = html.find("section", class_="item-download-options")
    for link in download_options.find_all('a', class_="format-summary download-pill"):
        if "PDF" in link.text:
            pdf_link = "https://archive.org" + link['href']
            break
    
    return pdf_link


def convert_to_image(path, pdf):

    pdf_name = pdf[:-4]

    print(f"\rConverting {pdf_name} to Images", flush=True, sep='', end='')
    print('')

    pages = convert_from_path(path+pdf, 350, poppler_path="C:\\Users\\vk\\Downloads\\Release-22.01.0-0\\poppler-22.01.0\\Library\\bin") 
    
    page_num = 0
    for page in pages:
        page_image_name = "page_" + str(page_num) + ".jpg"

        print(f"\r{page_image_name}", flush=True, sep='', end='')

        if not os.path.exists(f".\\pdf_images\\{pdf_name}\\"):
            os.makedirs(f".\\pdf_images\\{pdf_name}\\")

        page.save(f".\\pdf_images\\{pdf_name}\\" + pdf_name + "_" + page_image_name, 'JPEG')
        page_num += 1
    
    print('')
    
    return page_num


def extract_text(page_num, path, pdf):
    pdf_name = pdf[:-4]

    texts = []

    path = path + pdf_name + "\\"

    texts = {}

    print(f"\rExtracting text from {pdf_name}", flush=True, sep='', end='')
    print('')

    for i in range(page_num):
        page_image_name = "page_" + str(i) + ".jpg"
        
        print(f"\r{page_image_name}", flush=True, sep='', end='')

        page_image = Image.open(path + pdf_name + "_" +page_image_name)
        text = pytesseract.image_to_string(page_image, lang="mar+eng")

        t = texts.setdefault(i+1, text)
    
    print('')

    return texts




if __name__ == "__main__":

    csv_file = "./pdf_links.csv"
    page_links = get_links_from_csv(csv_file)

    print('')

    pages = []
    for link in page_links:
        page = {}
        if link.endswith(".pdf"):
            pdf_link = link
        else:
            print(f"\rScraping link -> {link}", end='')
            sys.stdout.flush()

            pdf_link = scrape_link(link)
        
        page.setdefault("page_link", link)
        page.setdefault("pdf_link", pdf_link)

        pages += [page]

    print('')


    
    pages = [pages[45], pages[39], pages[0], pages[1], pages[18]] # comment this line to run the program for all links


    # downloading PDFs
    for pdf in pages:
        pdf_name = download(pdf['pdf_link'])
        pdf.setdefault("pdf_name", pdf_name)
        print('')

    print('')




    # initialising output file
    output_file = open("OCR_TEXT_TEST_RUN.json", 'w')
    output_file.write('[')
    output_file.close()


    # extracting text from PDFs
    for pdf in pages:
        pdf_text = {}
        try:
            pdf_images = convert_to_image(".\\downloaded_pdfs\\", pdf['pdf_name'])
            pdf_text = extract_text(pdf_images, ".\\pdf_images\\", pdf['pdf_name'])
        except:
            pass

        pdf.setdefault("pdf_text", pdf_text)
        output_file = open("OCR_TEXT_TEST_RUN.json", 'a')
        output_file.write(json.dumps(pdf) + ",")
        output_file.close()

    
    # write output file
    output_file = open("OCR_TEXT_TEST_RUN.json", 'a')
    output_file.write("]")
    output_file.close()


    # removing trailing comma

    with open("./OCR_TEXT_TEST_RUN.json") as data:
        data = data.read()[:-2] + "]"
        data = json.loads(data)

    output_file = open("OCR_TEXT_TEST_RUN.json", 'w')
    output_file.write(json.dumps(data, indent=2))
    output_file.close()
