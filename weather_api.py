# main.py

# requests와 json 라이브러리 import
import requests
import json
import time

# API에서 데이터를 읽어오는 함수
def read_data_from_api(api_url, params):

    try:
        # 기온 : T1H
        # 1시간 강수량 : RN1
        # 습도 : RE1
        # 강수상태 :PTY

        # API에 요청을 보내고 응답을 받음
        response = requests.get(api_url, params=params)
        #print(response.text)

        # 응답 데이터를 JSON 형식으로 파싱
        json_data = response.json()

        # 'items' 배열에 접근
        items = json_data['response']['body']['items']['item']

        # 'T1H', 'RN1', 'RE1', 'PTY' 카테고리의 obsrValue 값을 변수로 저장
        t1h_value = None
        rn1_value = None
        re1_value = None
        pty_value = None

        for item in items:
            if item['category'] == 'T1H':
                t1h_value = item['obsrValue']
            elif item['category'] == 'RN1':
                rn1_value = item['obsrValue']
            elif item['category'] == 'REH':
                re1_value = item['obsrValue']
            elif item['category'] == 'PTY':
                pty_value = item['obsrValue']

        # 각 카테고리의 obsrValue 값을 변수에 저장
        print("T1H 값:", t1h_value)
        print("RN1 값:", rn1_value)
        print("RE1 값:", re1_value)
        print("PTY 값:", pty_value)

        response.close()
        # 기상청에서 수신받은 데이터 리턴(순서대로 기온, 강수량, 습도, 강수상태)
        return t1h_value, rn1_value, re1_value, pty_value 

    except KeyError as e:
        print("API 응답에서 예상대로 'body' 키가 없습니다:", e)
        return None, None, None, None
    except Exception as e:
        print("오류 발생:", e)
        return None, None, None, None

# 프로젝트를 실행하는 메인 함수
def main():
    my_key = 'xxSW9FhmJqYFW2R+f1wOpGU84rcA2GWCkaBpS82YFC8azuYLWjhw2LHJwwpEJSPtVJcvRB8sEn6CE7yWdfTKwQ=='
    api_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'


    # ThingSpeak 서버 URL
    # server_name = 'http://api.thingspeak.com/update'
    # ThingSpeak API 키
    # api_key = 'FW7TNGNTN7XDMH4G'
    # 헤더 설정
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    while True:

        # 현재 시간을 얻어옴
        current_time = time.localtime()

        # 현재 시간에서 한 시간을 뺀 후 시간 단위로 변환하여 systime 변수에 저장
        systime = str((current_time.tm_hour - 1) * 100)

        # 현재 날짜를 받아옴
        current_date = time.strftime("%Y%m%d")

        # 시간, 날짜 출력
        print("현재시각:", systime) 
        print("현재 날짜:", current_date)

        params = {'serviceKey' : my_key
                , 'pageNo' : '1'
                , 'numOfRows' : '1000'
                , 'dataType' : 'JSON'
                , 'base_date' : current_date
                , 'base_time' : systime
                , 'nx' : '55'
                , 'ny' : '127' }

        # read_data_from_api 함수 실행 및 반환값 받기
        t1h_value, rn1_value, re1_value, pty_value = read_data_from_api(api_url, params)
        
        # 요청 데이터 구성
        #http_request_data = {'api_key': api_key
        #                    , 'field1': t1h_value
        #                    , 'field2': rn1_value
        #                    , 'field3': re1_value
        #                    , 'field4': pty_value}

        # POST 요청 보내기
        #response = requests.post(server_name, data=http_request_data, headers=headers)

        # 응답 코드 확인
        #if response.status_code > 0:
        #    print("HTTP Response code:", response.status_code)
        #    print("성공")
        #else:
        #    print("Error code:", response.status_code)
        #    print("실패")
            
        time.sleep(20)  # 20초 대기


if __name__ == "__main__":
    main()