from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import re
import operator
from django.utils import timezone
import os
import sys
from nltk.probability import FreqDist
import csv
import sqlite3
from .models import Item

#중복되는경우 replace 되도록 해야할듯.

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
f = open('./csvfile.csv', 'w', encoding='utf-8', newline='')
csvWriter = csv.writer(f)
tokenizer = RegexpTokenizer(r'\w+')
en_stopwords = set(stopwords.words("english"))
en_stopwords.update(['beer','beers','tasted','body','beer','ml','bottle','like','much','less','l', 'taste', 'ratebeer', 'commercial', 'description'])


def crawling(url, country):
    CRAWLING_URL = url
    soup = crawler(url)
    global name, company, rate, content, img, description_

    style=""
    content = ""

    ##제품 이름 , 스타일 , 회사, 평점, 이미지 주소 크롤링(name, style, company, rate)
    table = soup.find("div", {"id":"myvar2"}).find_all("a")

    for idx, a in enumerate(table):
        if idx%2==1:
            style = a.get_text().strip()

        else:
            content = ""
            name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', a.get_text()).strip()
            link = 'https://www.ratebeer.com' + a['href']
            ##1페이지 리뷰 크롤링해서 파일에 저장
            soup_ = crawler(link)
            if (soup_.find('a', {'id':'_brand4'}) !=None):
                company = soup_.find('a', {'id':'_brand4'}).get_text()
            if (soup_.find('a', {'name' : 'real average'}) != None):
                rate = soup_.find('a', {'name' : 'real average'}).big.get_text()

            description = soup_.find('div', class_="commercial-description-container").div.get_text().strip()
            if description == "No commercial description" :
                description_ = ""
            else:
                description_ = filtering(description)

            if(soup_.find('img', {'itemprop' : 'image'})['src'] != ""):
                img = soup_.find('img', {'itemprop' : 'image'})['src']
            print(country + " : " +name+ " : "+company+" : "+img)

            ##리뷰가 없는 제품은 제외한다.
            try:
                if(soup_.find('div',class_='reviews-container') != None):
                    reviews = soup_.find('div',class_='reviews-container')
                    divs = reviews.div.div.find_all('div')
                    for idx, div in enumerate(divs):
                        if idx%4==3:
                            content += div.get_text()
                else:
                    continue
            except:
                return

            ##리뷰 페이지들(페이지가 2쪽 이상이면 2쪽부터 추출됨)
            try:
                if(soup_.find_all('a', class_="ballno") != None):
                    pages = soup_.find_all('a', class_="ballno")
                    for page in pages:
                        review_page = 'https://www.ratebeer.com'+ page['href']
                        soup_ = crawler(review_page)
                        reviews = soup_.find('div',class_='reviews-container')
                        divs = reviews.div.div.find_all('div')
                        for idx, div in enumerate(divs):
                            if idx%4==3:
                                content += div.get_text()
            except:
                continue

            #내용 필터링
            completed = filtering(content)

            csvWriter.writerow([name, country, company, style, rate, completed, description_])

            #DB에 저장할 경우
            insertDB(name, company, country, rate, description_, style, img)





def crawler(url):
    req = urllib.request.Request(url, headers = {'User-Agent' : 'Mozilla/5.0'})
    sourceCode = urllib.request.urlopen(req)
    soup = BeautifulSoup(sourceCode, 'lxml')
    return soup






def filtering(content):
    ##문장들을 단어로 자르고 특수문자, 불용어, 숫자 제거
    content = content.lower()
    tokens = tokenizer.tokenize(content)
    stopped_tokens = [i for i in tokens if not i in en_stopwords and len(i)>1]
    number_tokens = [re.sub(r'[\d]', '', i) for i in stopped_tokens]
    filtered = [i for i in number_tokens if i != '']

    ##가장 빈도수 많은 단어 30개만 저장
    completed = []
    fdist = FreqDist(filtered)
    for idx, word in enumerate(fdist.most_common(15)):
        completed.append(fdist.most_common(15)[idx][0])

    return completed

def insertDB(namee, companyy, countryy, ratee, descriptionn, stylee, img):
    item = Item(name = namee, company = companyy, country = countryy, style = stylee, created_date = timezone.now(), rate = ratee, description = descriptionn, img_url=img)
    item.save()



def main():
    print("crawl and save in CSV....\n")
    baseurl = 'https://www.ratebeer.com/beer/country/abkhazia/263/'
    soup = crawler(baseurl)

    ##264개국. 약 13200개  / 학습 데이터 208국가(A-V), 검증 데이터 56국가(W-Z)
    select = soup.find('select', {'id':'menu2'})
    urlList = select.find_all('option')


    for url in urlList:
        addr = url['value']
        country = url.get_text().strip()
        if addr == '0':
            continue
        else:
            searchUrl = 'https://www.ratebeer.com'+addr
            crawling(searchUrl, country)



    # urls = ['https://www.ratebeer.com/beer/country/south-korea/111/',
    # 'https://www.ratebeer.com/beer/country/japan/105/',
    # 'https://www.ratebeer.com/beer/country/united-states/213/',
    # 'https://www.ratebeer.com/beer/country/australia/14/',
    # 'https://www.ratebeer.com/beer/country/england/240/',
    # 'https://www.ratebeer.com/beer/country/canada/39/',
    # 'https://www.ratebeer.com/beer/country/china/45/',
    # 'https://www.ratebeer.com/beer/country/spain/183/',
    # 'https://www.ratebeer.com/beer/country/netherlands/144/',
    # 'https://www.ratebeer.com/beer/country/russia/169/',
    # 'https://www.ratebeer.com/beer/country/germany/79/',
    # 'https://www.ratebeer.com/beer/country/belgium/23/',
    # 'https://www.ratebeer.com/beer/country/hong-kong/93/']
    #
    # for url in urls:
    #     crawling(url)





if __name__ == '__main__':
    main()