
from ctypes.wintypes import PINT
from tokenize import Number, String
from bs4 import BeautifulSoup
import os
import xlwt as xt
import xlrd as xd
from nltk.util import ngrams
import re

# productName = "Kichen Utensil"
# productName = "Silicone Food Bag"
# productName = "Pepper Mill"
# productName = "French Press Coffee Maker"
# productName = "Coffee Grinder"
productName = "smart watch"

ALIEXPRESS_ABPATH=os.path.abspath(os.path.dirname(__file__))
PRODUCTLIST_HTML_PATH = ALIEXPRESS_ABPATH + "/OriginalData"
LIST_RESULT_DATA_PATH = ALIEXPRESS_ABPATH + "/ResultsData" 
PRODUCT_LIST_INFO_PATH = LIST_RESULT_DATA_PATH + "/ProductListInfo.xls"

TITLES = ["Title", "Rating", "Reviews", "Price", "ASIN", "Sponsored", "Html Name", "Link"]

class Product:
    title = ""
    orders = ""
    rating = ""
    price = ""
    link = ""
    ad = ""
    deals = ""
    freight = ""


def getHtml(file):
    return BeautifulSoup(open(file, "r", encoding='utf-8'), 'html.parser')


def clearText(list):
    if (len(list) > 0):
        return list[0].text.strip().replace("  ", "").replace("\n", "")
    else:
        return ""


def getHtmFile(folder=PRODUCTLIST_HTML_PATH, format=".html"):
    filesList = os.listdir(folder)
    htmFileslist = []

    for file in filesList:
        if (file.endswith(format) or file.endswith(".html")):
            htmFileslist.append(file)
    return htmFileslist


def getProductFromHtml(htmlSoup, htmlName):
    productHtmlWrapper = htmlSoup.select("div[class='JIIxO']")[0]
    productsHtml = productHtmlWrapper.select("a._3t7zg._2f4Ho")
    
    productList = []
    for prodcutHtml in productsHtml:
       product = Product()
       product.title = prodcutHtml.select("h1")[0].text
       if prodcutHtml.find("span", class_= "_31JQ_"):
        product.ad = prodcutHtml.select("span._31JQ_")[0].text
       else:
        product.ad = ""
       product.price = prodcutHtml.select("div.mGXnE._37W_B")[0].text
       if prodcutHtml.find("div", class_= "i0heB"):
        product.deals = prodcutHtml.select("div.i0heB")[0].text
       else:
        product.deals = ""
       if prodcutHtml.find("span", class_= "_1kNf9"):
        product.orders = prodcutHtml.select("span._1kNf9")[0].text
       else: 
         product.orders = ""
       if prodcutHtml.find("span", class_= "eXPaM"):
        product.rating = prodcutHtml.select("span.eXPaM")[0].text
       else: 
         product.rating = ""
       if prodcutHtml.find("span", class_= "_2jcMA"):
        product.freight = prodcutHtml.select("span._2jcMA")[0].text
       else: 
         product.freight = ""
       product.link = prodcutHtml["href"]       
       productList.append(product)
    return productList


def getProductListFromFiles():
    fileList = getHtmFile()
    
    productList = []
    for file in fileList:
        filePath = PRODUCTLIST_HTML_PATH + "/" + file
        htmlSoup = getHtml(filePath)
        products = getProductFromHtml(htmlSoup, file)
        productList = productList + products
    return productList

def saveProductTitle(productList):
    book = xt.Workbook(encoding='utf-8', style_compression=0)
    productSheet = book.add_sheet("Product", cell_overwrite_ok=True)
    sumPrice = 0
    sumOrders = 0
    sumAd = 0
    for index in range(len(productList)):

        sumPrice = sumPrice + float(str(productList[index].price).replace("US $", ""))
        if productList[index].orders != "" :
            sumOrders = sumOrders + int(str(productList[index].orders).replace(" sold", ""))         
        if productList[index].ad != "" : 
            sumAd = sumAd + 1 

        productSheet.write(index + 1, 0, productList[index].title)
        productSheet.write(index + 1, 1, productList[index].price)
        productSheet.write(index + 1, 2, productList[index].ad)
        productSheet.write(index + 1, 3, productList[index].deals)
        productSheet.write(index + 1, 4, productList[index].orders)
        productSheet.write(index + 1, 5, productList[index].rating)
        productSheet.write(index + 1, 5, productList[index].freight)
        productSheet.write(index + 1, 5, productList[index].rating)
    productSheet.write(0, 1, "avg:" + str(round(sumPrice / len(productList), 2)))
    productSheet.write(0, 2, "total ad rate:" + str(round(sumAd / len(productList), 2) * 100) + "%")
    productSheet.write(0, 4, "total order:" + str(sumOrders))
    book.save(PRODUCT_LIST_INFO_PATH)


def main():
    allProduct = getProductListFromFiles()
    saveProductTitle(allProduct)

main()
