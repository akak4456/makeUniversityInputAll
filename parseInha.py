#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
import re

driver = webdriver.Chrome('./chromedriver.exe')

#인하대학교
driver.get('http://sugang.inha.ac.kr/sugang/SU_51001/Lec_Time_Search.aspx')
select = Select(driver.find_element_by_id('ddlDept'))
html = driver.page_source

regex = re.compile("<option value=\"(\d{7})")
result_optionValue = regex.findall(html)

regex = re.compile("<option selected=\"selected\" value=\"(\d{7})")
result = regex.search(html).group(1)
result_optionValue.insert(0,result)

soup = BeautifulSoup(html,'html.parser')
result_major = soup.find_all("option")
for n in range(0,len(result_major)-len(result_optionValue)):
   result_major.pop()

#E-Learning 선택 막기
select = Select(driver.find_element_by_id('ddlDept'))
select.select_by_value(result_optionValue[1])
#E-Learning 선택 막기

content = [""]
count = 0
result_count = len(result_optionValue)
#len(result_optionValue)
for n in range(0,result_count):
   count = 0
   select = Select(driver.find_element_by_id('ddlDept'))
   select.select_by_value(result_optionValue[n])
   html = driver.page_source
   soup = BeautifulSoup(html,'html.parser')
   mr = soup.find_all("td")
   for object in mr:
      if object.get_text() != "Y" and object.get_text() != "N" and re.match("D\d{1,2}",object.get_text()) == None:
         content[n] += object.get_text()
         if count == 9:
            content[n] += "#"
            content[n] += result_major[n].get_text()
            content[n] += "$"
            count = -1
         else:
            content[n] += "#"
         count+=1
   content[n] += "@"
   content.append("")
result = "";
for n in range(0,result_count):
   result += content[n]

result = re.sub('\n|\t|\'|\"','',result)
#공백 문제되는 특수문자 제거완료
regex = re.compile(u"#셀0")
result = regex.sub("#0_0,0,0",result)
regex = re.compile(u"#월(\d)")
result = regex.sub("#1_\g<1>",result)
regex = re.compile(u"#화(\d)")
result = regex.sub("#2_\g<1>",result)
regex = re.compile(u"#수(\d)")
result = regex.sub("#3_\g<1>",result)
regex = re.compile(u"#목(\d)")
result = regex.sub("#4_\g<1>",result)
regex = re.compile(u"#금(\d)")
result = regex.sub("#5_\g<1>",result)
regex = re.compile(u"#토(\d)")
result = regex.sub("#6_\g<1>",result)
regex = re.compile(u"/월(\d)")
result = regex.sub("/1_\g<1>",result)
regex = re.compile(u"/화(\d)")
result = regex.sub("/2_\g<1>",result)
regex = re.compile(u"/수(\d)")
result = regex.sub("/3_\g<1>",result)
regex = re.compile(u"/목(\d)")
result = regex.sub("/4_\g<1>",result)
regex = re.compile(u"/금(\d)")
result = regex.sub("/5_\g<1>",result)
regex = re.compile(u"/토(\d)")
result = regex.sub("/6_\g<1>",result)
regex = re.compile(u"\,월(\d)")
result = regex.sub(u"(s)/1_\\g<1>",result)
regex = re.compile(u"\,화(\d)")
result = regex.sub(u"(s)/2_\\g<1>",result)
regex = re.compile(u"\,수(\d)")
result = regex.sub(u"(s)/3_\\g<1>",result)
regex = re.compile(u"\,목(\d)")
result = regex.sub(u"(s)/4_\\g<1>",result)
regex = re.compile(u"\,금(\d)")
result = regex.sub(u"(s)/5_\\g<1>",result)
regex = re.compile(u"\,토(\d)")
result = regex.sub(u"(s)/6_\\g<1>",result)
#요일 숫자화완료
f = open('inha.txt','w')
f.write(result)
f.close
print "inha done"

#인하대학교
