#!/usr/bin/env python

import urllib.request
from datetime import datetime, timedelta, time
import datetime as dt
import pandas as pd
import pickle

def get_ecdc_data():
    datetimeToday = datetime.today()
    date = datetimeToday.date() #μέρα τώρα
    time = datetimeToday.time() #ώρα τώρα
    yesterday = date - timedelta(1) #μέρα ώρα χθες
    yesterday = str(yesterday) #μέρα χθες
    timeFilter = dt.time(10, 00, 00) #ώρα που ανεβάζουν τα data
    print (timeFilter)
    filename = 'static/data/ecdcdata'
    if time<timeFilter:
        print ("...getting yesterday's results...")
        try:
            url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-'+yesterday+'.xls'
            urllib.request.urlretrieve(url, filename)
            print ('downloaded yesterdays xls')
        except:
            url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-'+yesterday+'.xlsx'
            urllib.request.urlretrieve(url, filename)
            print ('downloaded yesterdays xlsx')
    else:
        print ("...getting today's results...")
        try:
            url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-'+str(date)+'.xls'
            urllib.request.urlretrieve(url, filename)
        except:
            try:
                url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-'+str(date)+'.xlsx'
                urllib.request.urlretrieve(url, filename)
            except:
                print ('no data yet')

def map_countries():
    mapping = pickle.load(open('static/data/mapping','rb'))
    countries =[]
    lats=[]
    lons=[]
    for k,v in mapping.items():
        countries.append(k)
        lats.append(v[0])
        lons.append(v[1])
    df = pd.DataFrame()
    df['CountryExp']=countries
    df['lat']=lats
    df['lon']=lons
    return (df)

def merge_data():
    iso = pd.read_csv('static/data/iso.csv',names=['Country','iso2','iso3'])
    iso2dict = dict(zip(iso.iso2, iso.Country))
    iso3dict = dict(zip(iso.iso3, iso.Country))
    locs = map_countries()
    oldData = pd.read_excel('static/data/oldData.xls')
    eudict = dict(zip(oldData.GeoId,oldData.EU))
    get_ecdc_data()
    covid = pd.read_excel('static/data/ecdcdata',converters={'GeoId':str})
    countryExp = list()
    for i,r in covid.iterrows():
        try:
            if len(r['GeoId'])>2:
                countryExp.append(iso3dict[r['GeoId']])
            else:
                try:
                    countryExp.append(iso2dict[r['GeoId']])
                except KeyError:
                    countryExp.append('Other')
        except TypeError:
            countryExp.append('Namibia')
    covid['CountryExp'] = countryExp
    covid = covid.rename(columns={"Cases":"NewConfCases","Deaths":"NewDeaths"})
    covid['EU'] = covid['GeoId'].map(eudict)

    whr2019 = pd.read_csv('static/data/world-happiness-report-2019.csv')
    whr2019['CountryExp'] = whr2019['iso2'].map(iso2dict)
    whr2019 = whr2019.rename(columns={"Log of GDP\nper capita":"Log of GDP per capita","Healthy life\nexpectancy":"Healthy life expectancy"})

    df1 = pd.merge(covid,whr2019 , on="CountryExp",how='left')
    df = pd.merge(df1,locs,on="CountryExp",how='left')

    human_freedom = pd.read_csv('static/data/human_freedom.csv')
    human_freedom['CountryExp'] = human_freedom['ISO_code'].map(iso3dict)
    human_freedom = human_freedom.filter(['CountryExp', 'hf_score','ISO_code'])

    df_final = pd.merge(df,human_freedom,on="CountryExp",how='left')
    pickle.dump(df_final, open('static/data/df.pickle', 'wb'))

if __name__ == "__main__":
    merge_data()

