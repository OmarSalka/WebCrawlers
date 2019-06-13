# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

#imported the list of companies from the csv file to use for url alteration

# created the dataset "fortuneList" from the csv file
fortuneList = pd.read_csv("fortuneList.csv")

#created an array "fortuneArray" based off of the fortuneList dataset
fortuneArray = fortuneList.values

# generating the url list by combining the first portion of the url with the final parameter of the url, obtained from the csv file
urls = []
counter = -1
for i in fortuneArray:
    counter += 1
    #pulling the name from each array element in addition to reformatting it to a simple string
    newstr = str(fortuneArray[counter]).replace("['", "").replace("']", "")
    i = "http://fortune.com/fortune500/" + newstr
    urls.append(i)
    

'''--------------------Data Being Scraped-----------------'''

# General info
sector = []
industry = []
num_of_employees = []

# Key Financials (Last Fiscal Year) 
revenues_in_Ms = []
perc_change_in_revs = []
profits_in_Ms = []
perc_change_in_prof = []
assets_in_Ms = []
total_stockholder_equity_in_Ms = []
market_value_as_of_March_29_2018_in_Ms = []

#Profit Ratios
profit_as_perc_of_revs = []
profits_as_perc_of_assets = []
profits_as_perc_of_stockholder_equity = []

#Earnings Per Share (Last Fiscal Year)
earnings_per_share_USD = []
EPS_perc_change_from_2016 = []
EPS_perc_change_5_year_annual_rate = []
EPS_perc_change_10_year_annual_rate = []

#Total Return
total_return_to_investors_2017 = []
total_return_to_investors_5_year_annualized = []
total_return_to_investors_10_year_annualized = []


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
    sleep(randint(2, 7))
    
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
    #parsing the % change in revenues and appending to respective list
    perc_change_in_rev = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("company-data-Revenues ($M).2")}).text.replace("%", "").replace(",", "")
    if perc_change_in_rev == "":
        perc_change_in_rev = "-"
        perc_change_in_revs.append(perc_change_in_rev)
    else:
        perc_change_in_rev = float(perc_change_in_rev)
        perc_change_in_revs.append(perc_change_in_rev)
    
    #parsing the profits and appending to respective list
    profits = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("company-data-Profits ($M).1")}).text.replace(",", "").replace("$", "")
    if profits == "-":
        profits_in_Ms.append(profits)
    else:
        profits = float(profits)
        profits_in_Ms.append(profits)

    #parsing the % change in revenues and appending to respective list
    perc_change_in_p = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("company-data-Profits ($M).2")}).text.replace("%", "").replace(",", "")
    if perc_change_in_p == "":
        perc_change_in_p = "-"
        perc_change_in_prof.append(perc_change_in_p)
    else:
        perc_change_in_p = float(perc_change_in_p)
        perc_change_in_prof.append(perc_change_in_p)
    
    #parsing assets and appending to respective list
    assets = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("company-data-Assets ($M).1")}).text.replace(",", "").replace("$", "")
    if assets == "-":
        assets_in_Ms.append(assets)
    else:
        assets = int(assets)
        assets_in_Ms.append(assets)
    #parsing total stockholder equity and appending to respective list
    tse = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("company-data-Total Stockholder Equity ($M).1")}).text.replace(",", "").replace("$", "")
    if tse == "-":
        total_stockholder_equity_in_Ms .append(tse)
    else:
        tse = int(tse)
        total_stockholder_equity_in_Ms .append(tse)
    #parsing market value and appending to respective list
    market_value = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("company-data-Market Value — as of March 29, 2018 ($M).1")}).text.replace(",", "").replace("$", "")
    if market_value == "-":
        market_value_as_of_March_29_2018_in_Ms.append(market_value)
    else:
        market_value = int(market_value)
        market_value_as_of_March_29_2018_in_Ms.append(market_value)
    #parsing profit As Percent Of Revenues and appending to respective list
    profitAsPercentOfRevenues = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("Profit as % of Revenues-trow.2")}).text.replace("%", "").replace(",", "")
    if profitAsPercentOfRevenues ==  "-":
        profit_as_perc_of_revs.append(profitAsPercentOfRevenues)
    else:
        profitAsPercentOfRevenues = float(profitAsPercentOfRevenues)
        profit_as_perc_of_revs.append(profitAsPercentOfRevenues)
    
    #parsing profits As Percent Of Assets and appending to respective list
    profitsAsPercOfAssets = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("Profits as % of Assets-trow.2")}).text.replace("%", "").replace(",", "")
    if profitsAsPercOfAssets == "-":
        profits_as_perc_of_assets.append(profitsAsPercOfAssets)
    else:
        profitsAsPercOfAssets = float(profitsAsPercOfAssets)
        profits_as_perc_of_assets.append(profitsAsPercOfAssets)
    
    #parsing profits As Perc Of Stockholder Equity and appending to respective list
    profitsAsPercOfStockholderEquity = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("Profits as % of Stockholder Equity-trow.2")}).text.replace("%", "").replace(",", "")
    if profitsAsPercOfStockholderEquity == "-":
        profits_as_perc_of_stockholder_equity.append(profitsAsPercOfStockholderEquity)
    else:
        profitsAsPercOfStockholderEquity = float(profitsAsPercOfStockholderEquity)
        profits_as_perc_of_stockholder_equity.append(profitsAsPercOfStockholderEquity)
    
    #parsing earnings Per Share and appending to respective list
    earningsPerShare = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("Earnings Per Share ($)-trow.2")}).text.replace(",", "")
    if earningsPerShare == "-":
        earnings_per_share_USD.append(earningsPerShare)
    else:
        earningsPerShare = float(earningsPerShare)
        earnings_per_share_USD.append(earningsPerShare)

    #parsing EPS_PerChange and appending to respective list
    EPS_PercChangeFrom_2016 = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("EPS % Change (from 2016)-trow.2")}).text.replace("%", "").replace(",", "")
    if EPS_PercChangeFrom_2016 == "-":
        EPS_perc_change_from_2016.append(EPS_PercChangeFrom_2016)
    else:
        EPS_PercChangeFrom_2016 = float(EPS_PercChangeFrom_2016)
        EPS_perc_change_from_2016.append(EPS_PercChangeFrom_2016)

    #parsing EPS perc change (5_year_annual_rate) and appending to respective list
    EPS_PercChange_5_yearAnnualRate = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("EPS % Change (5 year annual rate)-trow.2")}).text.replace("%", "").replace(",", "")
    if EPS_PercChange_5_yearAnnualRate == "-":
        EPS_perc_change_5_year_annual_rate.append(EPS_PercChange_5_yearAnnualRate)
    else:
        EPS_PercChange_5_yearAnnualRate = float(EPS_PercChange_5_yearAnnualRate)
        EPS_perc_change_5_year_annual_rate.append(EPS_PercChange_5_yearAnnualRate)

    #parsing EPS perc change (10_year_annual_rate) and appending to respective list
    EPS_PercChange_10_yearAnnualRate = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("EPS % Change (10 year annual rate)-trow.2")}).text.replace("%", "").replace(",", "")
    if EPS_PercChange_10_yearAnnualRate == "-":
        EPS_perc_change_10_year_annual_rate.append(EPS_PercChange_10_yearAnnualRate)
    else:
        EPS_PercChange_10_yearAnnualRate = float(EPS_PercChange_10_yearAnnualRate)
        EPS_perc_change_10_year_annual_rate.append(EPS_PercChange_10_yearAnnualRate)

    #parsing total return to investors 2017 and appending to respective list
    totalReturnToInvestors_2017 = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("Total Return to Investors (2017)-trow.2")}).text.replace("%", "").replace(",", "")
    if totalReturnToInvestors_2017 == "-":
        total_return_to_investors_2017.append(totalReturnToInvestors_2017)
    else:    
        totalReturnToInvestors_2017 = float(totalReturnToInvestors_2017)
        total_return_to_investors_2017.append(totalReturnToInvestors_2017)
    
    #parsing Total Return to Investors (5 year, annualized) and appending to respective list
    totalReturnToInvestors_5_yearAnnualized = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("Total Return to Investors (5 year, annualized)-trow.2")}).text.replace("%", "").replace(",", "")
    if totalReturnToInvestors_5_yearAnnualized == "-":
        total_return_to_investors_5_year_annualized.append(totalReturnToInvestors_5_yearAnnualized)
    else:
        totalReturnToInvestors_5_yearAnnualized = float(totalReturnToInvestors_5_yearAnnualized)
        total_return_to_investors_5_year_annualized.append(totalReturnToInvestors_5_yearAnnualized)
    
    #parsing Total Return to Investors (10 year, annualized) and appending to respective list
    totalReturnToInvestors_10_yearAnnualized = webpage_html.find("td", {"data-reactid": lambda L: L and L.endswith("Total Return to Investors (10 year, annualized)-trow.2")}).text.replace("%", "").replace(",", "")
    if totalReturnToInvestors_10_yearAnnualized == "-":
        total_return_to_investors_10_year_annualized.append(totalReturnToInvestors_10_yearAnnualized)
    else:
        totalReturnToInvestors_10_yearAnnualized = float(totalReturnToInvestors_10_yearAnnualized)
        total_return_to_investors_10_year_annualized.append(totalReturnToInvestors_10_yearAnnualized)

company_Name = []
index = -1
for i in fortuneArray:
    index += 1
    company = str(fortuneArray[index]).replace("['", "").replace("']", "")
    company_Name.append(company)

   
#converting to a dataset
fortune_500 = pd.DataFrame({'company_Name': company_Name,
                            'sector': sector,
                              'industry': industry,
                              'num_of_employees': num_of_employees,
                              'revenues_in_Ms': revenues_in_Ms,
                              'perc_change_in_revs': perc_change_in_revs,
                              'profits_in_Ms': profits_in_Ms,
                              'perc_change_in_prof': perc_change_in_prof,
                              'assets_in_Ms': assets_in_Ms,
                              'total_stockholder_equity_in_Ms': total_stockholder_equity_in_Ms,
                              'market_value_as_of_March_29_2018_in_Ms': market_value_as_of_March_29_2018_in_Ms,
                              'profit_as_perc_of_revs': profit_as_perc_of_revs,
                              'profits_as_perc_of_assets': profits_as_perc_of_assets,
                              'profits_as_perc_of_stockholder_equity': profits_as_perc_of_stockholder_equity,
                              'earnings_per_share_USD': earnings_per_share_USD,
                              'EPS_perc_change_from_2016': EPS_perc_change_from_2016,
                              'EPS_perc_change_5_year_annual_rate': EPS_perc_change_5_year_annual_rate,
                              'EPS_perc_change_10_year_annual_rate': EPS_perc_change_10_year_annual_rate,
                              'total_return_to_investors_2017': total_return_to_investors_2017,
                              'total_return_to_investors_5_year_annualized': total_return_to_investors_5_year_annualized,
                              'total_return_to_investors_10_year_annualized': total_return_to_investors_10_year_annualized})
    
fortune_500.to_csv("fortune_500_V2.csv")

