import streamlit as st

st.title("🎈 덕인중학교 급식 검색")
pip install openai
import os
import openai
import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 목포덕인중학교 코드 설정
EDUCATION_OFFICE_CODE = "F10"  # 전라남도교육청 코드
SCHOOL_CODE = "F100000120"      # 목포덕인중학교 코드

# 급식 데이터 가져오기 함수
def get_school_lunch(school_code, education_office_code, date):
    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=YOUR_API_KEY&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE={education_office_code}&SD_SCHUL_CODE={school_code}&MLSV_YMD={date}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'mealServiceDietInfo' in data:
            df = pd.json_normalize(data['mealServiceDietInfo'][1]['row'])
            return df
        else:
            return None
    else:
        return None

# GPT를 사용한 메뉴 설명과 팁 생성 함수
def generate_menu_tips(menu):
    prompt = f"Explain the menu item '{menu}' and provide tips on how to enjoy it deliciously."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides detailed menu descriptions and tips on how to enjoy them."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response['choices'][0]['message']['content']
    return answer

# Streamlit 앱
st.title("목포덕인중학교 급식 검색")

# 날짜 입력 받기
date = st.date_input("날짜를 선택하세요", datetime.today())

# 급식 정보 가져오기
if st.button("검색"):
    df = get_school_lunch(SCHOOL_CODE, EDUCATION_OFFICE_CODE, date.strftime("%Y%m%d"))
    
    if df is not None and not df.empty:
        st.write(df[['MMEAL_SC_NM', 'DDISH_NM']])  # 급식 종류와 메뉴 출력
        
        # 각 메뉴에 대한 설명과 팁 생성
        menus = df['DDISH_NM'].iloc[0].split(" ")
        for menu in menus:
            st.subheader(menu)
            description_and_tip = generate_menu_tips(menu)
            st.write(description_and_tip)
    else:
        st.error("급식 데이터를 가져오는 데 실패했습니다.")
git add app.py
git commit -m "Integrate OpenAI API to generate menu descriptions and tips"
git push origin main
streamlit==1.26.0
pandas==2.1.1
requests==2.31.0
openai==0.28.0
