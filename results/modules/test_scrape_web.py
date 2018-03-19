#imports
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time
    
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

'''for obj in list:
        obj.getPrice()'''
    


def amazon(amazon_url, pr):
    
    
    page_soup = webClient(amazon_url)

    #img can be found with this?: container[0].findAll("span")
    containers = page_soup.findAll("div", {"class":"s-item-container"})
    print(len(containers))
    pretty = page_soup.prettify()
    for container in containers:
        #Grabs brand
        try:
            brand = container.findAll("span", {"class":"a-size-small a-color-secondary"})[1].text
        except IndexError:
            brand = "Brand Unavaliable"

        #brabs name
        try:
            name = container.h2.text
        except IndexError:
            name = "Name Unavalibale"

        #Grabs image
        try:
            img = container.img["src"]
        except IndexError:
            img = "Image Unavaliable"

        #grabs link
        link = container.a["href"]

        #Grabs price - two different ways it can be displayed
        try:
            price = container.findAll("span", {"class":"a-size-base a-color-price s-price a-text-bold"})[0].text
        except IndexError:
            #price = "Price Unavalibale"
            

            try:
                price = container.findAll("span", {"class":"a-size-base a-color-price a-text-bold"})[0].text
            except IndexError:
                price = "Price Unavalibale"


        price = price.replace("£", "")
        price = price.replace(",", "")
        if "-" in price:
            split_price = price.split("-")
            price = split_price[0]
        try:
            price = float(price)
            price = "%.2f" % price
            f_price = float(price)
            if f_price >= pr[0] and f_price <= pr[1]:
                #checks if its in price range
                product_list.append(["Amazon", name, brand, price, img, link])
        except ValueError:
            pv_list.append(["Amazon/pv", name, brand, price, img, link])
            
        '''print("Amazon", name, brand, price, img, link)
        print()
        print()'''
    return page_soup

        


       



def newegg(newegg_url, pr):
    
    page_soup = webClient(newegg_url)
    
    containers = page_soup.findAll("div", {"class":"item-container"})
    for container in containers:
        '''#grabs code of product
        code = container.find('ul', {'class':'item-features'})
        code = code.findAll('li')
        itera = 0
        for li in code:
            if 'Item #:' in li.strong.text:
                code = code[itera].text
                code = code[8:len(code)]
                print(code)
                times += 1
                #print(code[itera])
                break
            itera += 1'''

        
        #grabs brand
        try:
            brand = container.div.div.a.img["title"]
        except (AttributeError, TypeError):
            brand = "Brand Unavailable"

        #grabs name
        try:
            title = container.findAll("a", {"class":"item-title"})
            name = title[0].text
        except IndexError:
            name = "Name Unavaliable"

        #grabs price
        try:
            price_pounds = container.find("li", {"class":"price-current"}).strong.text
            price_pence = container.find("li", {"class":"price-current"}).sup.text
            price = price_pounds + price_pence
        except (AttributeError, TypeError):
            price = "Price Unavailable"
        price = price.replace(",", "")

        #grabs image
        img = "http:" + container.a.img["src"]

        #grabs link
        try:
            #link = container.div.a["href"] --old version
            link = container.find("a", {"class":"item-title"})["href"]
        except IndexError:
            link = "Link Unavaliable"

        try:
            price = float(price)
            price = "%.2f" % price
            f_price = float(price)
            if f_price >= pr[0] and f_price <= pr[1]:
                #checks if its in price range
                product_list.append(["Newegg", name, brand, price, img, link])
        except ValueError:
            pv_list.append(["Newegg/pv", name, brand, price, img, link])


def currys(currys_url, pr):
    
    page_soup = webClient(currys_url)
    
    #this way is for most cases where multiple options are presented
    try:
        results = page_soup.find("div", {"data-component":"product-list-view"})
        containers = results.findAll("article")
        
        containers = containers[1:len(containers)]
        for container in containers:
            try:
                name = container.find('span', {'data-product':'name'}).text
            except IndexError:
                name = 'Name Unavaliable'
            try:
                brand = container.find('span', {'data-product':'brand'}).text
            except IndexError:
                brand = 'Brand Unavaliable'
            try:
                img = container.find('img', {'class':'image'})['src']
            except IndexError:
                img = "Image Unavlaiable"

            try:
                link = container.find('header', {'class':'productTitle'}).a['href']
            except:
                link = "Link Unavaliable"
            try:
                price = container.find('strong', {'data-product':'price'}).text.strip()
                strip_price = ''
                for ch in price:
                    try:
                        int(ch)
                        strip_price += ch
                    except:
                        pass
                    if ch == '.':
                        strip_price += ch

                price = strip_price
            except:
                price = "Price Unavaliable"

            try:
                price = float(price)
                price = "%.2f" % price
                f_price = float(price)
                if f_price >= pr[0] and f_price <= pr[1]:
                    #checks if its in price range
                    product_list.append(["Currys", name, brand, price, img, link])
            except ValueError:
                pv_list.append(["Currys/pv", name, brand, price, img, link])
                
    except AttributeError:
        #this is for if currys takes you to the item itself
        page = page_soup.find('h1', {'class':'page-title nosp'})
        name = page.findAll('span')[0].text + ' ' + page.findAll('span')[1].text

        brand = page.findAll('span')[0].text

        link = currys_url

        img = page.find('img', {'class':'product-image'})['src']

        
        page = page_soup.find('div', {'class':'product-page'})
        price = page.find('strong', {'class':'current'}).text 

        strip_price = ''
        for ch in price:
            try:
                int(ch)
                strip_price += ch
            except:
                pass
            if ch == '.':
                strip_price += ch

        price = strip_price
        try:
            price = float(price)
            price = "%.2f" % price
            f_price = float(price)
            if f_price >= pr[0] and f_price <= pr[1]:
                #checks if its in price range
                product_list.append(["Currys", name, brand, price, img, link])
        except ValueError:
            pv_list.append(["Currys/pv", name, brand, price, img, link])


def maplin(maplin_url, pr):
    
    page_soup = webClient(maplin_url)
    results = page_soup.find("div", {"class":"products-container"})
    try:
        containers = results.findAll("div", {"class":"col-xs-8 col-sm-8 col-md-9 right-panel"})
    except:
        return

    maplin_product_list = []
    maplin_product_list_pv = []
    maplin_img_list = []
    
    for container in containers:
        #grabs code of item
        '''code = container.find('p', {'class':'item-code'}).text
        code = code[6:len(code)]
        print(code)'''

        #grabs name
        try:
            name = container.div.h4.text.strip()
        except IndexError:
            name = "Name Unavalibale"


        #grabs brand - unavailable

        #grabs link
        try:
            link = "http://www.maplin.co.uk" + container.div.h4.a["href"]
        except IndexError:
            link = "Link Unavailable"

        #grabs price
        try:
            price = container.find("div", {"class":"price-tag clearfix"}).h3.text[1:]
            price = price.replace(",", "")
            f_price = float(price)
            if f_price >= pr[0] and f_price <= pr[1]:
                #checks if its in price range
                maplin_product_list.append(["Maplin", name, "Brand Unavailable", price, "img", link])
        except (IndexError, AttributeError):
            price = "Price Unavalibale"
            maplin_product_list_pv.append(["Maplin/pv", name, "Brand Unavailable", price, "img", link])
    
    try:
        containers = results.findAll("div", {"class":"col-xs-4 col-sm-4 col-md-3 left-panel"})

        for container in containers:
            #grabs img
            img = "http:" + container.div.a.img["src"]
            #img = "http:" + img
            maplin_img_list.append(img)
            #print(img)
    except:
        pass

    i = 0
    for product in maplin_product_list:
        #print(priduct + "\n")
        product_list.append([product[0], product[1], product[2], product[3], maplin_img_list[i], product[5]])
        i += 1

    i = 0
    for product in maplin_product_list_pv:
        #print(priduct + "\n")
        pv_list.append([product[0], product[1], product[2], product[3], maplin_img_list[i], product[5]])
        i += 1

    # container of text is : col-xs-8 col-sm-8 col-md-9 right-panel
    # containers = page_soup.find("div", {"class":"products-container"})
    #a[1].div.h4.text.strip()

product_list = []
pv_list = []

def main(scrape_info):
    del product_list[:]
    del pv_list[:]
    
    while True:
        #my_url = input("What product would you like to search for: ")
        my_url = scrape_info["name"]

        #print("We are seraching for your prodcut, this won't take long")

        plus_word = my_url.replace(" ", "+")
        space_word = my_url.replace(" ", "%20")
        spaceB_word = my_url.replace(" ", "%2B")
        amazon_url = "https://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=" + plus_word + "&Trh=i%3Aaps%2Ck%" + space_word
        newegg_url = "https://www.newegg.com/global/uk/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=" + plus_word+"&N=-1&isNodeId=1"
        #currys_url = "https://www.currys.co.uk/gbuk/apple-phones-broadband-and-sat-nav/mobile-phones-and-accessories/mobile-phones/362_3412_32041_267_xx/xx-criteria.html?s=iphone"
        #currys_url =  "https://www.currys.co.uk/gbuk/search-keywords/xx_xx_xx_xx_xx/charger/xx-criteria.html"
        currys_url = "https://www.currys.co.uk/gbuk/search-keywords/xx_xx_xx_xx_xx/" + spaceB_word + "/xx-criteria.html"
        maplin_url = "https://www.maplin.co.uk/search/?text=" + space_word
        
        #page_soup = webClient(amazon_url)
        
        price_range = scrape_info["price_range"]
        #pretty = amazon(amazon_url, price_range)
        newegg(newegg_url, price_range)
        #currys(currys_url, price_range)
        maplin(maplin_url, price_range)
        
        #sorts list and prints it
        t1 = time.time()
        data_list = sorted(product_list, key=lambda x:float(x[3]))
        t2 = time.time()
        print(1000*(t2-t1))
        #data_list = product_list
        itera = 0
        for index in data_list:
            index.append(str(itera))
            itera += 1
       
            
       
       
   
        print(len(data_list))
        return {'product_list':[data_list, pv_list], 'data_list':data_list}
        #return [data_list, pv_list]
        '''for data in data_list:
            print("Website: ", data[0])
            print("Name: ", data[1])
            print("Brand: ", data[2])
            print("Price: ", data[3])
            print("Image: ", data[4])
            print("link: ", data[5])
            print()
            
        for price in pv_list:
            print("Website: ", price[0])
            print("Name: ", price[1])
            print("Brand: ", price[2])
            print("Price: ", price[3])
            print("Image: ", price[4])
            print("link: ", price[5])
            print()'''

    #scrape links from websites
    #5 differnt wesbites - maplin, newegg, amazon, currys?, ebyer?
    #sort out website


