import json
import os
import xlwt as xt
import xlrd as xd
from nltk.util import ngrams
import math
import random
TAGCLASS = "architecture_models"
EXCELNAME = os.path.dirname(__file__)+ "/keyWords.xls"
KEYWORDSFIELD = os.path.dirname(__file__)+ "/keywords.text"
KEYWORDJSON = os.path.dirname(__file__)+ "/keywords.json"

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
   return item[1] >0
    

def prepareData(content):
    keyWordsObject = countKeyWords(clearContent(content))
    sortKWS = sorted(keyWordsObject.items(), key=lambda x: (x[1], x[0]), reverse=True)
    filterKWS = filter(filterKWSFun, sortKWS)
    return list(filterKWS)


def putWordsToExcel(keyWordsArray, excelFile):
    
    # keyWordsBook = xd.open_workbook(excelFile)
    # keyWordsSheet = keyWordsBook.add_sheet(TAGCLASS, cell_overwrite_ok=True)
    keyWordsBook = xt.Workbook(encoding='utf-8', style_compression=0)
    keyWordsSheet = keyWordsBook.add_sheet(TAGCLASS, cell_overwrite_ok=True)
    rowIndex=0
    for item in keyWordsArray:
        keyWordsSheet.write(rowIndex, 0, item[0])
        keyWordsSheet.write(rowIndex, 1, item[1])
        keyWordsSheet.write(rowIndex, 2, TAGCLASS)
        rowIndex = rowIndex + 1

    keyWordsBook.save(EXCELNAME)

def generateHashTag(kws):
    step = math.ceil(len(kws)/3)
    highFrequency=random.sample(kws[f2:step],5)
    middleFrequency = random.sample(kws[step+1:step+step+1], 10)
    lowFrequency = random.sample(kws[step+step+1:len(kws)-1], 5)
    hashTagArray = kws[0:2]+lowFrequency+middleFrequency+highFrequency
    hashTagString = ""
    for item in hashTagArray:
       hashTagString = hashTagString +" #" +item[0]
    print(hashTagString)

def getDataFromExcel(filePath):
    keyWordsBook = xd.open_workbook(filePath)
    keywordsSheet = keyWordsBook.sheet_by_index(0)
    kwArray = []
    for rowIndex in range(keywordsSheet.nrows):
        kwArray.append((keywordsSheet.row_values(rowIndex)[0], keywordsSheet.row_values(rowIndex)[1]))
    return kwArray
def saveKeyWordsToJson(data):
     jsonData = { "data": data}
     with open(KEYWORDJSON,"w") as f:
       json.dump(jsonData,f)
       print("加载入文件完成...")
def getJsonFromExcel(filePath):
        keyWordsBook = xd.open_workbook(filePath)
        keywordsSheet = keyWordsBook.sheet_by_index(0)
        kwArray = []
        for rowIndex in range(keywordsSheet.nrows):
            kwArray.append({"word": keywordsSheet.row_values(rowIndex)[0], "count":keywordsSheet.row_values(rowIndex)[1], "chinese":keywordsSheet.row_values(rowIndex)[2], "rootWord":keywordsSheet.row_values(rowIndex)[3]})
        return kwArray
def main():
    # generate data
    #  fileContent = getfile(KEYWORDSFIELD)
    #  keyWordsArray = prepareData(fileContent)
    #  putWordsToExcel(keyWordsArray, EXCELNAME)

    #  kwFromExcel = getDataFromExcel(EXCELNAME)
    #  generateHashTag(kwFromExcel)

    # generate json file
     wordJson = getJsonFromExcel(EXCELNAME)
     saveKeyWordsToJson(wordJson)
     

main()
