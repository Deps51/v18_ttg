#imports
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

    
def webClient(my_url):
    try:
        #open web client
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()
    except:
        webClient(my_url)

    #parsing
    page_soup = soup(page_html, "html.parser")
    return page_soup

def newegg(newegg_url):
    
    page_soup = webClient(newegg_url)
    
    code = page_soup.find('em').text
    print(code)
    
    return code



def maplin(maplin_url):
    
    page_soup = webClient(maplin_url)
    
    code = page_soup.find('span', {'itemprop':'sku'}).text
    print(code)
    
    return code


def main(link, website):

    
    if 'Newegg' in website: 
        product_id = newegg(link)
    elif 'Maplin' in website:
        product_id = maplin(link)
  
    return product_id



