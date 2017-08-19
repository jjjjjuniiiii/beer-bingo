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

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
f = open('./csvfile.csv', 'w', encoding='utf-8', newline='')
csvWriter = csv.writer(f)
tokenizer = RegexpTokenizer(r'\w+')
en_stopwords = set(stopwords.words("english"))
en_stopwords.update(['thanks','abv','fermentation','carbonation','well','favorite','pours','since','nice','alcohol','import','taste','body','beer','ml','bottle','like','much','less','l', 'head', 'ratebeer', 'commercial', 'description','ingredients'])


def crawling(url, country):
    CRAWLING_URL = url

    soup = crawler(url)

    global name, company, rate, content, img, description_

    style=""
    content = ""
    description_ = ""


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
            else:
                continue

            if (soup_.find('a', {'name' : 'real average'}) != None):
                rate = soup_.find('a', {'name' : 'real average'}).big.get_text()

            description = soup_.find('div', class_="commercial-description-container").div.get_text().strip()
            if description == "No commercial description" :
                description_ = ""
            else:
                if(isEnglish(description) == True):
                    description_ = filtering(description, 3)

            img = soup_.find('img', {'itemprop' : 'image'})['src']
            try:
                urllib.request.urlopen(img)
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    img = "no_image.jpg"
                    pass




            ##리뷰가 없는 제품은 제외한다.
            try:
                if(soup_.find('div',class_='reviews-container') != None):
                    reviews = soup_.find('div',class_='reviews-container')
                    divs = reviews.div.div.find_all('div')
                    for idx, div in enumerate(divs):
                        if idx%4==3:
                            temp = div.get_text()
                            if(isEnglish(temp) == True):
                                content += temp
                            else:
                                continue
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
                                temp = div.get_text()
                                if(isEnglish(temp) == True):
                                    content += temp
                                else:
                                    continue
            except:
                continue

            #내용 필터링
            completed = filtering(content, 15)
            completed += description_

            if completed:
                print(country + " : " +name+ " : "+company)
                insertDB(name, company, country, rate, completed, style, img)

            #DB에 저장할 경우, 리스트에 글이 있는 경우만 저장
            #


def insertDB(namee, companyy, countryy, ratee, descriptionn, stylee, imgg):
    item = Item(name = namee, company = companyy, country = countryy, style = stylee, created_date = timezone.now(), rate = ratee, description = descriptionn, img_url = imgg)
    item.save()



def crawler(url):

    try:
        req = urllib.request.Request(url, headers = {'User-Agent' : 'Mozilla/5.0'})
        sourceCode = urllib.request.urlopen(req)
        soup = BeautifulSoup(sourceCode, 'lxml')
        return soup
    except urllib.error.HTTPError as e:
        if e.code == 408:
            pass
    except UnicodeEncodeError :
        pass


def isEnglish(text):
    try:
        s = text
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True



def filtering(content, num):
    filtered = ""
    ##문장들을 단어로 자르고 특수문자, 불용어, 숫자 제거
    content = content.lower()
    tokens = tokenizer.tokenize(content)
    stopped_tokens = [i for i in tokens if not i in en_stopwords and len(i)>3]
    number_tokens = [re.sub(r'[\d]', '', i) for i in stopped_tokens]
    for word in number_tokens:
        if word!= '':
            filtered += word+" "


    ##가장 빈도수 많은 단어 30개만 저장

    fdist = FreqDist(filtered)
    for idx, word in enumerate(fdist.most_common(num)):
        filtered += fdist.most_common(num)[idx][0]

    return filtered




def main():
    print("crawl and save in CSV....\n")
    baseurl = 'https://www.ratebeer.com/beer/country/azerbaijan/16/'
    soup = crawler(baseurl)

    ##264개국. 약 13200개  / 학습 데이터 208국가(A-V), 검증 데이터 56국가(W-Z)
    select = soup.find('select', {'id':'menu2'})
    urlList = select.find_all('option')


    #특정국가부터 시작, 숫자는 국가순일때 차례번호로 지정
    #urlList = urlList[181:len(urlList)]  #latvia

    for url in urlList:
        addr = url['value']
        country = url.get_text().strip()
        if addr == '0':
            continue
        else:
            searchUrl = 'https://www.ratebeer.com'+addr
            crawling(searchUrl, country)

    f.close()


if __name__ == '__main__':
    main()