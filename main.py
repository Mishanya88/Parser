import requests
from bs4 import BeautifulSoup
import progressbar
import json

def print_list(lst):
    print("{:<2} {:<20} {:<10} {:<15} {:<15}".format('№','Name' ,'Symbol','Price', 'Market_cap'))
    i = 1
    for str in lst:
        print("{:<2} {:<20} {:<10} {:<15} {:<15}".format(str['id'],str['Name'], str['Symbol'], str['Price'], str['Market-Cap']))
        i+=1


def Splitting(elements):
    elements_text = ''
    for i in range(0,2):
        if elements[i] is None:
            continue
        elif elements_text == '':
            elements_text = elements[i].text
    return elements_text


def pars10(Elements_list):
    url = 'https://coinmarketcap.com'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    coins = soup.find("tbody").find_all("tr")
    j = 0
    for i in coins:
        name = i.find(class_="sc-4984dd93-0 kKpPOn").text
        Element_Symbol = i.find(class_="sc-4984dd93-0 iqdbQL coin-item-symbol").text
        Element_Price = i.find_all('span')[1].text
        Element_Market = i.find(class_="sc-edc9a476-1 gqomIJ").text

        Elements_list.append({
            'id':j+1,
            'Name': name,
            'Symbol': Element_Symbol,
            'Price': Element_Price,
            'Market-Cap': Element_Market
        })
        j+=1
        if j == 10:
            break


def parse(Elements_list,count):
    bar = progressbar.ProgressBar(max_value=count,
                                  widgets=widgets).start()
    url = 'https://coinmarketcap.com'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    coins = soup.find("tbody").find_all("tr")
    j = 0
    for i in coins:
        Element_Name = [i.find(class_="sc-4984dd93-0 kKpPOn"),i.find_all('span')[3]]
        f = i.find(class_="cmc-link").get("href")
        url += f

        page2 = requests.get(url)
        soup2 = BeautifulSoup(page2.text, 'html.parser')
        market = [soup2.find(class_="statsValue"),soup2.find(class_="sc-8755d3ba-0 eXRmzO base-text")]
        url = url.replace(f, "")
        Element_Symbol = [i.find(class_="sc-4984dd93-0 iqdbQL coin-item-symbol"),i.find(class_="crypto-symbol")]
        Element_Price = [i.find_all('span')[1],i.find_all('span')[5]]
        Elements_list.append({
                'id':j+1,
                'Name': Splitting(Element_Name),
                'Symbol': Splitting(Element_Symbol),
                'Price': Splitting(Element_Price),
                'Market-Cap': Splitting(market)
        })
        bar.update(j)
        j += 1
        if j == count:
            break
    bar.finish()

def find(list,key):
    # for str in list:
    #     if (str['Name'] == key):
    #         print("{:<12} {:<10} {:<15} {:<15}".format(str['Name'], str['Symbol'], str['Price'], str['Market-Cap']))
    L = 0
    R = len(list) - 1
    list_sorted = sorted(list, key=lambda x: x['Name'])
    while (L < R):
        m = (L + R) // 2
        if list_sorted[m]['Name'] < key:
            L = m + 1
        else:
            R = m
    if list_sorted[R]['Name'] == key:
        print("{:<2} {:<12} {:<10} {:<15} {:<15}".format('№', 'Name', 'Symbol', 'Price', 'Market_cap'))
        print("{:<2} {:<12} {:<10} {:<15} {:<15}".format(list_sorted[R]['id'],list_sorted[R]['Name'], list_sorted[R]['Symbol'], list_sorted[R]['Price'], list_sorted[R]['Market-Cap']))
    else:
        print("Cryptocurrency not found\n")


if __name__ == '__main__':
    widgets = ['Progress:',
               progressbar.Bar('*'),
               progressbar.Counter(format=' %(value)02d/%(max_value)d '),
               progressbar.Timer(format='%(elapsed)s'),
               ]
    flag = False
    key = input('1)1-10 Crypto,\n2)1-100 Crypto,\nF) to find crypto coin by name,\nQ to quit\nInput: ')
    while key!= 'Q':
        if key == 'F' and flag == True:
            coin_name = input('Enter a crypto coin name to get info\nInput: ')
            find(Elements_list,coin_name)
        if key == '1':
            Elements_list = []
            pars10(Elements_list)
            print_list(Elements_list)
            flag = True
        if key == '2':
            Elements_list = []
            N = input('Number of cryptocurrencies 1 to 100\nInput: ')
            try:
                n = int(N)
                if n < 1 or n > 100:
                    print('<0 or >100')
                else:
                    parse(Elements_list, n)
                    print("\n")
                    print_list(Elements_list)
                    flag = True
            except:
                if N.isalpha():
                    print("Only number")
        if key == '3' and flag == True:
            print_list(Elements_list)
        key = input('1)1-10 Crypto,\n2)1-100 Crypto,\n3)Print List\nF) to find crypto coin by name,\nQ to quit\nInput: ')


