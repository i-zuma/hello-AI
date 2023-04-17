import openai
import json
import requests
import streamlit as st
import os
from dotenv import load_dotenv

#load_dotenv()

key = os.environ.get('OPENAI_API_KEY')
rapidKey = os.environ.get('RAPID_API_KEY')
openai.api_key = key
email = "hozayen@gmail.com"

def BasicGeneration(userPrompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": userPrompt}]
    )
    return completion.choices[0].message.content

st.set_page_config(page_title="البيتكوين اليوم - تحليل باستخدام الذكاء الإصطناعي", page_icon="🥇", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.markdown("""<style>
    .block-container{
    direction: rtl;}
    </style>""" ,unsafe_allow_html=True)

st.title('تحليل البيتكوين باستخدام الذكاء الإصطناعي')
st.subheader(
    'تحليل كريبتو مفصل لآخر 7 أيام')
#st.write('OPENAI Key: ', key)

st.warning(
    'تنبيه: هذا التحليل هو فقط من باب الافادة ولا يعد نصيحة مالية بأي حال. يرجى التدقيق والاطلاع قبل أي عملية شراء أو بيع')


def GetBitCoinPrices():    
    # Define the API endpoint and query parameters
    url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"
    #st.write(rapidKey)
    querystring = {
        "referenceCurrencyUuid": "yhjMzLPhuIDl",
        "timePeriod": "7d"
    }
    
    #st.info(rapidKey)
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
    with st.spinner('قد تستغرق العملية بعض الوقت.\n جاري التحليل...'):
        chatGPTPrompt = f"""You are an expert crypto trader with more than 10 years of experience, 
                    I will provide you with a list of bitcoin prices for the last 7 days
                    can you provide me with a technical analysis in correct Arabic for both the copy and the headings
                    of Bitcoin based on these prices. here is what I want: 
                    Price Overview, 
                    Moving Averages,
                    Resistance and support, 
                    Relative Strength Index (RSI),
                    Moving Average Convergence Divergence (MACD),
                    Advice and Suggestion,
                    Do I buy or sell?
                    Bull or bear market?
                    Please be as detailed as much as you can, and explain in a way any beginner can understand. Show your analysis for USD and no other currencies.
                    For style, make sure to use headings as bullet points and leave three line breaks before each new bullet point. For numbers, use 'commas' as a separator for thousands everywhere and round numbers to 2 decimal points
                    Here is the price list: {bitcoinPrices}"""
    
        analysis = BasicGeneration(chatGPTPrompt)
        st.text_area("التحليل", analysis,
                     height=500)
        
        st.markdown(f'لديك اقتراح أو تعليق؟ <a href="mailto:{email}?subject=أداة تحليل البيتكوين">أرسل هنا </a>', unsafe_allow_html=True)
        #st.snow()
        #st.success('تم!')
