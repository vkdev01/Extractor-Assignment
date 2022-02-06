import json
import requests
from bs4 import BeautifulSoup
import html5lib
import fire

def crawl(link):
  result =""
  article = requests.get(link).text
  article = BeautifulSoup(article, 'html5lib')
  content = article.find('div', id="bodyContent").find('div', class_="mw-parser-output")
  for para in content.find_all('p')[0:2]:
    if para.has_attr('class') and "mw-empty-elt" in para.get('class'):
      continue
    result += para.text
  return result


def scrape(keyword, links):
  keyword = keyword.replace(" ","+")

  search_link = f"https://en.wikipedia.org/w/index.php?title=Special:Search&limit={links}&offset=0&search={keyword}"

  html = requests.get(search_link).text
  html = BeautifulSoup(html, 'html5lib')

  results = html.find("div", id="mw-search-top-table")
  results = results.find("div", class_="results-info").text
  results = results.split(" ")
  results = results[-1].replace(',', '')
  print("Total results = ", int(results))

  pages = html.find('div', id="mw-content-text", class_="mw-body-content")
  pages = html.find("div", class_="searchresults").ul.find_all('li', class_="mw-search-result")

  outputs = []

  for page in pages:
    anchor = page.find('div', class_="mw-search-result-heading").a

    heading = anchor['title']
    link = "https://en.wikipedia.org" + anchor['href']
    page_data = page.find('div', class_="mw-search-result-data").text

    result = crawl(link)

    output = {
        'title': heading,
        'url' : link,
        'page_details': page_data,
        'paragraph' : result
    }

    outputs += [output]

  return outputs


# print(json.dumps(outputs, indent = 1))


def get_args(keyword=None, links=25, output="out"):
  """
  Takes keyword to search, number of links to crawl and name of output file without extension.
  """

  if keyword is None:
      print("keyword is Required")
  if links == 0:
    print("Enter number of links to crawl")
  else:
      output = output.replace('.', '_')+".json"

      outs = scrape(keyword, links) # searching keywords and crawling links

      # write output file
      output_file = open(output, 'w')
      output_file.write(json.dumps(outs, indent = 2))
      output_file.close()

      print(keyword, links, output)


if __name__ == "__main__":
  fire.Fire(get_args)