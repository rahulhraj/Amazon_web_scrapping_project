from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

#function to extract description
def get_description(soup):
    
    try:
        description=soup.find("span",attrs={"id",'productTitle'})
        description_value=description.text
        description_string=description_value.strip()

    except AttributeError:
        description_string=""

    return description_string

#function to get ASIN
def get_ASIN(soup):

    try:
        asin=soup.find("td",attrs={"class","a-size-base prodDetAttrValue"}).string.strip()
    
    except AttributeError:
        asin=""

    return asin

#function to get product description
def get_proddescription(soup):

    try:      
        prod_desc=soup.find("span",attrs={"class","a-list-item"}).string.strip()

    except AttributeError:
        prod_desc=""

    return prod_desc

#function to get manufacturer name
def get_manufacturer(soup):

    try:
        manufacturer=soup.find("a",attrs={"id","bylineInfo"})

    except AttributeError:
        manufacturer=""

    return manufacturer

if __name__=='__main__':

    hdr=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0','Accept-Language': 'en-US, en;q=0.5'})

    url_list=[]
    for k in range(1,21):

        url='https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'+str(k)
        url_list.append(url)
    
    d={"Description":[],"ASIN":[],"Product Description":[],"Manufacturer":[]}
    
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

            d["Description"].append(get_description(new_soup))
            d["ASIN"].append(get_ASIN(new_soup))
            d['Product Description'].append(get_proddescription(new_soup))
            d["Manufacturer"].append(get_manufacturer(new_soup))
    
    amazon_df=pd.DataFrame.from_dict(d)
    amazon_df.to_csv("amazon_data_2.csv",header=True, index=False)