import bs4
import requests
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

@app.get("/gold_price")
def request() :
    web = requests.get('https://www.goldtraders.or.th/UpdatePriceList.aspx')
    soup = bs4.BeautifulSoup(web.text , "html.parser")
    table = soup.find('table',{'id':'DetailPlace_MainGridView'})
    tr = table.find_all('tr')
    output = {}
    count = 1
    for data in tr[2:] :
        data_dict = {}
        array_name = ['เวลา','ครั้งที่','ทองแท่งรับซื้อ (บาท)','ทองแท่งขายออก (บาท)','ทองรูปพรรณรับซื้อ (บาท)','ทองรูปพรรณขายออก (บาท)','Gold Spot','Baht / US$','ขึ้น / ลง']
        count_value = 0
        for value in data.find_all('td') :
            data_dict[array_name[count_value]] = value.text
            count_value = count_value + 1
        output[count] = data_dict
        count = count + 1
    return output

@app.get("/calendar")
def request() :
    url = 'https://th.investing.com'
    web = requests.get(url + '/economic-calendar')
    soup = bs4.BeautifulSoup(web.text , "html.parser")
    table = soup.find('table',{'id':'economicCalendarData'})
    tr = table.find_all('tr')
    output = {}
    count = 1
    for data in tr[3:] :
        data_dict = {}
        array_name = ['เวลา','สกุลเงิน','ความสำคัญ','เหตุการณ์','ค่าจริง','คาดการณ์','ครั้งก่อน','อ้างอิง']
        count_value = 0
        counter = 0
        max_count_value = 7
        link_value = 3
        for value in data.find_all('td') :
            if count_value <= max_count_value :
                if count_value != 2 :
                    if count_value == link_value or count_value == len(array_name) - 1 :
                        if counter == 0 :
                            data_dict[array_name[count_value]] = str(value.text).replace(' ','').replace('\n','')
                            counter = counter + 1
                        else :
                            data_dict[array_name[count_value]] = str(url + str(data.find_all('td')[3].find('a')['href']))
                    else :
                        data_dict[array_name[count_value]] = str(value.text).replace(' ','').replace('\n','')
                else :
                    data_dict[array_name[count_value]] = len(data.find_all('td')[count_value].find_all('i',{'class':'grayFullBullishIcon'}))
                count_value = count_value + 1
        output[count] = data_dict
        count = count + 1
    return output

@app.get("/association")
def request() :
    data = {'เวลา': None,'ข้อมูล':{'ทองคำแท่ง 96.5%':{"ขายออก":None,'รับซื้อ':None},"ทองรูปพรรณ 96.5%":{"ขายออก":None,"ฐานภาษี":None}}}
    web = requests.get('https://www.goldtraders.or.th/')
    soup = bs4.BeautifulSoup(web.text , "html.parser")
    content = soup.find('div',{'id':'DetailPlace_uc_goldprices1_GoldPricesUpdatePanel'})
    data['เวลา'] = content.find_all('table')[0].find('span',{'id':"DetailPlace_uc_goldprices1_lblAsTime"}).find('font').text
    table = content.find_all('table')[1]
    tr = table.find_all('tr')
    data['ข้อมูล']['ทองคำแท่ง 96.5%']['ขายออก'] = tr[0].find_all('td')[2].find('span').find('b').find('font').text
    data['ข้อมูล']['ทองคำแท่ง 96.5%']['รับซื้อ'] = tr[1].find_all('td')[2].find('span').find('b').find('font').text
    data['ข้อมูล']['ทองรูปพรรณ 96.5%']['ขายออก'] = tr[2].find_all('td')[2].find('span').find('b').find('font').text
    data['ข้อมูล']['ทองรูปพรรณ 96.5%']['ฐานภาษี'] = tr[3].find_all('td')[2].find('span').find('b').find('font').text
    return data

@app.get("/XAU-USD")
def request() :
    web = requests.get('https://www.investing.com/currencies/xau-usd')
    soup = bs4.BeautifulSoup(web.text , "html.parser")
    data_test = soup.find_all('div', attrs={'data-test' : True})
    for data_test_select in data_test :
        if data_test_select['data-test'] == 'key-info' :
            div = data_test_select.find_all('div')
            Bid = div[1].find('dd').find('span').find_all('span')[1].text
            Ask = div[4].find('dd').find('span').find_all('span')[1].text
            return {'bid':Bid,'ask':Ask}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3456)