# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 09:55:48 2018

@author: I870266
"""

import pandas as pd

#imported the list of companies from the csv file to use for url alteration

# created the dataset "fortuneList" from the csv file
global_links = pd.read_csv("C:/Users/I870266/Desktop/pythonProjects/global_500_links.csv")

#created an array "fortuneArray" based off of the fortuneList dataset
links_Array = global_links.values
# generating the url list by combining the first portion of the url with the final parameter of the url, obtained from the csv file
urls = []
counter = -1
for i in links_Array:
    counter += 1
    #pulling the name from each array element in addition to reformatting it to a simple string
    newstr = str(links_Array[counter]).replace("['", "").replace("']", "")
    urls.append(newstr)
    

'''--------------------Data Being Scraped-----------------'''

# General info
Company_Name = []
HQ_Location = []
sector = []
industry = []
num_of_employees = []

# Key Financials (Last Fiscal Year) 
revenues_in_Ms = []
profits_in_Ms = []
market_value_as_of_March_29_2018_in_Ms = []


#to make requests
from requests import get

#to pace the execution of iterations
from time import sleep

#to generate random numbers
from random import randint

#to clear past outputs and display the most recent one of them
from IPython.display import clear_output


#to generate time
from time import time

#to parse the HTML content
from bs4 import BeautifulSoup

#to use the warn object that'll warn when an error occurs
from warnings import warn

start_time = time()
request_num = 0
counter = -1

for i in urls:
    counter += 1
    i = urls[counter]
    response = get(i)
    
    #pausing the loop
    sleep(randint(2, 5))
    
    #monitoring the requests
    request_num += 1
    elapsed_time = time() - start_time
    #we'll clear the output after each iteration, and replace it with information about the most recent request
    clear_output(wait = True)
    print('Request#: {}; Frequency: {} requests/s'.format(request_num, request_num/elapsed_time), end = "\r")
    
    #throw a warning for a non-200 status code (if the request was unsuccessful, throw a warning)
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(request_num, response.status_code))
        
    #break the loop if the # of requests exceeded the # expected
    if request_num > 499:
        warn("number of requests was greater than expected!")
        break
    
    #to parse the content of the request w/ BeautifulSoup
    webpage_html = BeautifulSoup(response.text, "html.parser")
    
    '''---------------------------parsing section below------------------------------'''
    
    #parsing the sector name and appending to respective list
    sector_element = webpage_html.find("p", {"data-reactid": lambda L: L and L.endswith("Sector.1.0")}).text
    sector.append(sector_element)
    
    #Company Name
    Company = webpage_html.find("h1").text
    Company_Name.append(Company)
    
    #HQ Location
    HQ = webpage_html.find("p", {"data-reactid": lambda L: L and L.endswith("HQ Location.1.0")}).text
    HQ_Location.append(HQ)
    
    #parsing the industry name and appending to respective list
    industry_element = webpage_html.find("p", {"data-reactid": lambda L: L and L.endswith('Industry.1.0')}).text
    industry.append(industry_element)
    
    #parsing the employees number and appending to respetive list
    employee_element = webpage_html.find("p", {"data-reactid": lambda L: L and L.endswith("Employees.1.0")}).text.replace(",", "")
    if employee_element == "" or "-" or "n/a":
        num_of_employees.append(employee_element)
    else:
        employee_element = int(employee_element)
        num_of_employees.append(employee_element)

    #parsing the revenues figure and appending to respective list
    revenues = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("company-data-Revenues ($M).1")}).text.replace(",", "").replace("$", "")
    if revenues == "-":
        revenues_in_Ms.append(revenues)
    else:
        revenues = int(revenues)
        revenues_in_Ms.append(revenues)
        
    #parsing the profits and appending to respective list
    profits = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("company-data-Profits ($M).1")}).text.replace(",", "").replace("$", "")
    if profits == "-":
        profits_in_Ms.append(profits)
    else:
        profits = float(profits)
        profits_in_Ms.append(profits)
        

   
#converting to a dataset
global_500 = pd.DataFrame({'Company_Name': Company_Name,
                              'HQ_Location': HQ_Location,
                              'sector': sector,
                              'industry': industry,
                              'num_of_employees': num_of_employees,
                              'revenues_in_Ms': revenues_in_Ms,
                              'profits_in_Ms': profits_in_Ms
                              })
    
global_500.to_csv("global_500.csv")
















