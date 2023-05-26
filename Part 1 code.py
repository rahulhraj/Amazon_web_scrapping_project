from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

#function to extract product title
def get_title(soup):
    
    try:
        title=soup.find("span",attrs={"id",'productTitle'})
        title_value=title.text
        title_string=title_value.strip()

    except AttributeError:
        title_string=""

    return title_string

#function to extract product price
def get_price(soup):
    
    try:
        price=soup.find("span",attrs={"class","a-price-whole"}).string.strip()

    except AttributeError:

        try:
            price=soup.find("span",attrs={"class","a-offscreen"}).string.strip()
        
        except:
            price=""
    
    return price

#function to extract rating
def get_rating(soup):

    try:
        rating=soup.find("span",attrs={"class","a-icon a-icon-star a-star-4-5 cm-cr-review-stars-spacing-big"}).string.strip()

    except AttributeError:
        try:
            rating=soup.find("span",attrs={"class","a-icon-alt"}).string.strip()

        except:
            rating=""
    return rating

#function to extract number of reviews
def get_numberofreviews(soup):

    try:
        review_num=soup.find("soup",attrs={"id","acrCustomerReviewText"}).string.strip()

    except AttributeError:
        review_num=""
    
    return review_num

if __name__=='__main__':

    hdr=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0','Accept-Language': 'en-US, en;q=0.5'})
    
    url_list=[]
    for k in range(1,21):

        url='https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'+str(k)
        url_list.append(url)
    
    d={"Product URL":[],"Product Name":[],"Product Price":[],"Product ratings":[],"Number of reviews":[]}

    for URL in url_list:

        webpage=requests.get(URL,headers=hdr)
        soup=BeautifulSoup(webpage.content,"html.parser")
        links=soup.find_all("a",attrs={"class","a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

        link_lists=[]
        for link in links:
            link_lists.append(link.get('href'))
        
        for l in link_lists:
            new_webpage=requests.get("https://www.amazon.in"+l,headers=hdr)
            new_soup=BeautifulSoup(new_webpage.content,"html.parser")
            
            d['Product URL'].append("https://www.amazon.in"+l)
            d['Product Name'].append(get_title(new_soup))
            d['Product Price'].append(get_price(new_soup))
            d['Product ratings'].append(get_rating(new_soup))
            d['Number of reviews'].append(get_numberofreviews(new_soup))
    
    amazon_df=pd.DataFrame.from_dict(d)
    amazon_df.to_csv("amazon_data.csv",header=True, index=False)

