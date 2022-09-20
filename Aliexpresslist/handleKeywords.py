import os
import xlwt as xt
import xlrd as xd
from nltk.util import ngrams
import math
import random

ALIEXPRESS_ABPATH=os.path.abspath(os.path.dirname(__file__))
LIST_RESULT_DATA_PATH = ALIEXPRESS_ABPATH + "/ResultsData" 
PRODUCT_LIST_TITLE_NGRAMS = LIST_RESULT_DATA_PATH + "/ProductListTitleNgrams.xls"

def getfile(filePath):
    return open(filePath).read()

def checkKeyWords(kw):
    if(kw != ""):
        return True
    else:
        return False

def countKeyWords(kws):
    countObject = {}
    for item in kws:
        if item not in countObject:
            countObject[item] = 1
        else:
            countObject[item] += 1
    return countObject

def clearContent(content):
   return content.replace(" ", "").replace("\n", "").split("#")

def filterKWSFun(item):
   return item[1] >1
    

def prepareData(content):
    keyWordsObject = countKeyWords(clearContent(content))
    sortKWS = sorted(keyWordsObject.items(), key=lambda x: (x[1], x[0]), reverse=True)
    filterKWS = filter(filterKWSFun, sortKWS)
    return list(filterKWS)


def putWordsToExcel(keyWordsArray, excelFile):

    keyWordsBook = xd.open_workbook(excelFile)
    keyWordsSheet = keyWordsBook.add_sheet("KeyWords_temporary", cell_overwrite_ok=True)
    # titleString = ""
    # for rowIndex in range(titlesSheet.nrows):
    #     titleString = titleString + "  " + titlesSheet.row_values(rowIndex)[0]
    # pat_letter = re.compile(r'[^a-zA-Z \']+')
    # titleString = pat_letter.sub(' ', titleString).strip().lower()
    # return titleString.split()

    # keyWordsBook = xt.Workbook(encoding='utf-8', style_compression=0)
    # keyWordsSheet = keyWordsBook.add_sheet("KeyWords", cell_overwrite_ok=True)
    rowIndex=0
    for item in keyWordsArray:
        keyWordsSheet.write(rowIndex, 0, item[0])
        keyWordsSheet.write(rowIndex, 1, item[1])
        rowIndex = rowIndex + 1

    keyWordsBook.save("keyWords.xls")

def generateHashTag(kws):
    step = math.ceil(len(kws)/3)
    print(step)
    highFrequency=random.sample(kws[1:step], 3)
    middleFrequency = random.sample(kws[step+1:step+step+1], 4)
    lowFrequency = random.sample(kws[step+step+1:len(kws)-1], 3)
    hashTagArray = kws[0:2]+lowFrequency+middleFrequency+highFrequency
    hashTagString = ""
    for item in hashTagArray:
       hashTagString = hashTagString +" " +item[0]
    print(hashTagString)

def getDataFromExcel(filePath):
    keyWordsBook = xd.open_workbook(filePath)
    keywordsSheet = keyWordsBook.sheet_by_index(0)
    kwArray = []
    for rowIndex in range(keywordsSheet.nrows):
        if(keywordsSheet.row_values(rowIndex)[1] > 2):
          kwArray.append((keywordsSheet.row_values(rowIndex)[0], keywordsSheet.row_values(rowIndex)[1]))
    return kwArray

def main():
    # fileContent = getfile("./china_traditional_architecture_keywords.text")
    # keyWordsArray = prepareData(fileContent)
    kwFromExcel = getDataFromExcel(PRODUCT_LIST_TITLE_NGRAMS)
    generateHashTag(kwFromExcel)
    # putWordsToExcel(keyWordsArray, "./keyWords.xls")


main()
