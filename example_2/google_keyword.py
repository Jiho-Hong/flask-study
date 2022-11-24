import requests
from bs4 import BeautifulSoup


def get_search_count(keyword):
    url = "https://www.google.com/search?q={}".format(keyword)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text)
    number = soup.select_one('#result-stats').text
    number = number[number.find('약')+2:number.rfind('개')]
    number = int(number.replace(',', ''))
    return {'keyword': keyword, 'number': number}


if __name__ == '__main__':
    print(get_search_count("튜토리얼"))
