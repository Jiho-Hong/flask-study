import requests
from datetime import datetime, timedelta
from pprint import pprint  # 구조있는 데이터를 더 편하게 보여줌


def get_weather(nx=62, ny=126):
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
    service_key = ""

    # 웹 요청할 base_date, base_time 계산
    now = datetime.now()  # 현재 시각 데이터 생성

    # 40분 이전이면 현재 시보다 1시간 전 `base_time`을 요청한다.
    if now.minute <= 40:
        # 단. 00:40분 이전이라면 `base_date`는 전날이고 `base_time`은 2300이다.
        if now.hour == 0:
            base_date = (now-timedelta(days=1)).strftime('%Y%m%d')
            base_time = '2300'
        else:
            base_date = now.strftime('%Y%m%d')
            base_time = (now-timedelta(hours=1)).strftime('%H00')
    # 40분 이후면 현재 시와 같은 `base_time`을 요청한다.
    else:
        base_date = base_date = now.strftime('%Y%m%d')
        base_time = now.strftime('%H00')
    # print(base_date, base_time)

    # 웹 요청시 같이 전달될 데이터 = 요청 메시지
    params = {
        'serviceKey': service_key,
        'numOfRows': 30,
        'pageNo': 1,
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny
    }

    res = requests.get(url=url, params=params)
    # print(res.status_code, type(res.text), res.url)
    # print()
    # print(res.text)

    # 응답 데이터 정리
    data = res.json()  # json.loads(res.text)와 같은 기능
    data = data['response']['body']['items']['item']
    # pprint(data)

    # category 표
    categorys = {
        'T1H': '기온',
        'RN1': '1시간 강수량',
        'UUU': '동서바람성분',
        'VVV': '남북바람성분',
        'REH': '습도',
        'PTY': '강수형태',
        'VEC': '풍향',
        'WSD': '풍속',
    }

    # 최종 데이터 생성
    results = {}
    for d in data:
        results[categorys[d['category']]] = d['obsrValue']
    # pprint(results)
    return results


if __name__ == "__main__":
    print(get_weather())
