import openai
import json
import requests
import streamlit as st
import os
from dotenv import load_dotenv


key = os.environ.get('OPENAI_API_KEY')
rapidKey = os.environ.get('X-RapidAPI-Key')
openai.api_key = key

def BasicGeneration(userPrompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": userPrompt}]
    )
    return completion.choices[0].message.content

st.set_page_config(page_title="البيتكوين اليوم - تحليل باستخدام الذكاء الاصطناعي", page_icon="🥇", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.markdown("""<style>
    .block-container{
    direction: rtl;}
    </style>""" ,unsafe_allow_html=True)

st.title('تحليل البيتكوين باستخدام الذكاء الاصطناعي')
st.subheader(
    'تحليل كريبتو مفصل لآخر 7 أيام')
st.write(
    'تنبيه: هذا التحليل هو فقط من باب الافادة ولا يعد نصيحة مالية بأي حال. يرجى التدقيق والاطلاع قبل أي عملية شراء أو بيع')


def GetBitCoinPrices():    
    # Define the API endpoint and query parameters
    url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"
    rapidKey = os.environ.get('X-RapidAPI-Key')
    
    querystring = {
        "referenceCurrencyUuid": "yhjMzLPhuIDl",
        "timePeriod": "7d"
    }
    
    # Define the request headers with API key and host
    headers = {
        "X-RapidAPI-Key": rapidKey,
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }
    
    # Send a GET request to the API endpoint with query parameters and headers
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    
    # Parse the response data as a JSON object
    JSONResult = json.loads(response.text)
    
    # Extract the "history" field from the JSON response
    history = JSONResult["data"]["history"]
    
    # Extract the "price" field from each element in the "history" array and add to a list
    prices = []
    for change in history:
        prices.append(change["price"])
    
    # Join the list of prices into a comma-separated string
    pricesList = ','.join(prices)
    
    # Return the comma-separated string of prices
    return pricesList
    
if st.button('ابدأ التحليل'):
    with st.spinner('جاري تحميل أسعار البتكوين...'):
        bitcoinPrices = GetBitCoinPrices()
        #st.success('!تم')
    with st.spinner('قد تستغرق العملية بعض الوقت. جاري التحليل...'):
        chatGPTPrompt = f"""You are an expert crypto trader with more than 10 years of experience, 
                    I will provide you with a list of bitcoin prices for the last 7 days
                    can you provide me with a technical analysis in UAE Arabic
                    of Bitcoin based on these prices. here is what I want: 
                    Price Overview, 
                    Moving Averages, 
                    Relative Strength Index (RSI),
                    Moving Average Convergence Divergence (MACD),
                    Advice and Suggestion,
                    Do I buy or sell?
                    Please be as detailed as much as you can, and explain in a way any beginner can understand. and make sure to use headings as bullet points
                    Here is the price list: {bitcoinPrices}"""
    
        analysis = BasicGeneration(chatGPTPrompt)
        st.text_area("التحليل", analysis,
                     height=500)
        st.success('تم!')
