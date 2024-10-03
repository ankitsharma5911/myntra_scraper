import os
import time
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import  pandas as pd


searchString = "pant"
searchString = searchString.replace(" ","-")

myntra = "https://www.myntra.com/" + searchString

print(myntra)
#Initialize the chrome Webdriver

driver = webdriver.Chrome()

# Navigate to URL
driver.get(myntra)

myntra_text = driver.page_source
myntra_html = bs(myntra_text,"html.parser")

smallbox = myntra_html.findAll("li",{"class":"product-base"})
print(len(smallbox))


df = pd.DataFrame(columns=['title','rating','price'])

try:


    for i in range(len(smallbox)):
        link = smallbox[i].a['href']
        productLink = "https://www.myntra.com/" +link
        print(productLink)

        

        driver.get(productLink)
        prodRes = driver.page_source
        prod_html = bs(prodRes,"html.parser")
        
        # title
        print("title..")
        title =prod_html.findAll("title")
        title = title[0].text
        print(title)

        # data['name'] = title

        # rating
        print("rating..")
        overallRating = prod_html.findAll("div",{"class":"index-overallRating"})

        rating = overallRating[0].div
        overallRating = float(rating.text)
        print(overallRating)
        # data['rating'] =overallRating
        print("price..")
        # price
        price = prod_html.findAll("span",{"class":"pdp-price"})
        price = price[0].strong.text
        print(price)

        print('saving data')
        
        df.loc[i] = [title, overallRating ,price]
        print('saving data complete')
        # review


        reviews = prod_html.findAll("a",{"class":'detailed-reviews-allReviews'})
        reviewslink = reviews[0]["href"]
        Review_link='https://www.myntra.com'+ reviewslink
        Review_link

        # open chrome for each review
        driver.get(Review_link)
        review_page=driver.page_source

        review_html = bs(review_page,"html.parser")

        review = review_html.findAll("div",{"class":'detailed-reviews-userReviewsContainer'})

        print("review start..")
        for i in review:
            user_rating = review.findAll("div",{"class":"user-review-main user-review-showRating"})

            user_comment = review.findAll("div",{"class":"user-review-reviewTextWrapper"})
            
            user_name = review.findAll("div",{"class":"user-review-left"})
            print(user_name)

        for i in range(len(user_rating)):
            rating = user_rating[i].div.span.text
            print(rating)


        for i in range(len(user_comment)):
            comment = user_comment[i].text
            print(comment)


        for i in range(len(user_name)):
            name = user_name[i].span.text
            print(name)

    
except Exception as e:
    print(e)
df.to_csv(f"data/{searchString}.csv") 
driver.close()




