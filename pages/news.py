from bs4 import BeautifulSoup as BS
import requests as req
import streamlit as st
st.header("Latest financial news:")

def scrape():
    url = "https://www.moneycontrol.com/news/" 
    #url = "https://www.businesstoday.in/latest/economy"

    webpage = req.get(url)
    trav = BS(webpage.content, "html.parser")
    M = 1
    output = "Latest financial news from this week:\n"
    for link in trav.find_all('a'):
        if(str(type(link.string)) == "<class 'bs4.element.NavigableString'>"
        and len(link.string) > 35):
            output += (str(M) + ". " + link.string + "\n")
            st.write(str(M)+".", link.string)
            M += 1
    with open("pages/finance_tracker_data/newsdata.txt", "w") as f:
        f.write(output)

if st.button("Scrape News"):
    scrape()