import requests
import bs4
import urllib2
import os
import glob
import csv
import codecs
from xlsxwriter.workbook import Workbook

url = "https://www.icodata.io/ICO/ended"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Referer': 'https://cssspritegenerator.com',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}
		 
req = urllib2.Request(url,headers=hdr)
page = urllib2.urlopen(req)
content = page.read()
soup = bs4.BeautifulSoup(content,'lxml')

with open('ICOData.csv','w') as file:
    wr = csv.writer(file,quoting=csv.QUOTE_ALL)
    for tb in soup.find_all('tbody'):
        for tr in soup.find_all('tr'):
            cell_list=[]
            for td in tr.find_all(['th','td']):
                cell_list.append(td.text.strip())
            wr.writerow(cell_list)

for csvfile in glob.glob(os.path.join('.', 'ICOData.csv')):
    workbook = Workbook(csvfile[:-4] + '.xlsx')
    worksheet = workbook.add_worksheet()
    with codecs.open(csvfile, 'rb', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r,c,col)
    workbook.close() 
