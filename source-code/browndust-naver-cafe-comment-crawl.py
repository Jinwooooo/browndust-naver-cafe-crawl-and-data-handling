# importing required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time

def get_n_child_index(lastCounter, currentCounter):
    nextPageChildPos = -1
    currentSector = int(currentCounter/10)
    if(currentSector == 0):
        nextPageChildPos = currentCounter + 1
    else:
        nextPageChildPos = ((currentCounter%10) + 2) + 1
    return(nextPageChildPos)

df = pd.DataFrame(columns=['user_ID','unit_voted'])
dfIndexCounter = 1
r = re.compile('.*\/.*')
lastIndex = int(input('Last Comment Page : '))

print('\n')
print('----------------------------------------------------------')
print('|                   Crawling Start...                    |')
print('----------------------------------------------------------')

driver = webdriver.Chrome()

driver.get('http://cafe.naver.com/browndust/ArticleRead.nhn?clubid=28708849&menuid=16&articleid=217084')
condition = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#post_217084')))
driver.switch_to_frame('cafe_main')

for pageIndex in range(0, lastIndex):
    time.sleep(3)
    commentList = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#cmt_list')))
    splitCommentList = (commentList.text).split('\n')
    splitCommentList = list(filter(r.match, splitCommentList))

    for elements in splitCommentList:
        splitElement = elements.split('/')
        userID = splitElement[0].replace(' ','')
        unitVoted = splitElement[1].replace(' ','')
        data = pd.DataFrame({'user_ID': userID, 'unit_voted': unitVoted}, index=[dfIndexCounter])
        df = pd.concat([df,data])
        dfIndexCounter += 1

    print('comment Page ' + str(pageIndex+1) + ' complete...')

    if(pageIndex != (lastIndex - 1)):
        nextPageChildPos = get_n_child_index(lastIndex, pageIndex)
        nextPageXPath = '//*[@id="cmt_paginate"]/a[' + str(nextPageChildPos) + ']'
        nextPageCrawl = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, nextPageXPath)))
        nextPageCrawl.send_keys(webdriver.common.keys.Keys.SPACE)
        nextPageCrawl.click()


print('\n')
print('----------------------------------------------------------')
print('|                   Crawling Complete                    |')
print('----------------------------------------------------------')
print('\n')
print('**********************************************************')

df.to_csv('~/Desktop/browndust-costume-event-crawled-comment.csv', sep=',', encoding='utf-8')
