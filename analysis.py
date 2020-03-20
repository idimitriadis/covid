import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import requests
import pickle
import urllib.request

def get_ecdc_data():
    datetimeToday = datetime.today()
    date = datetimeToday.date() #μέρα τώρα
    time = datetimeToday.time() #ώρα τώρα
    yesterday = date - timedelta(1) #μέρα ώρα χθες
    yesterday = str(yesterday) #μέρα χθες
    import datetime as dt
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
    return df_final

def get_dates(df):
    df = df[pd.notnull(df['DateRep'])]
    df['DateRep']=df['DateRep'].astype(str)
    df = df.sort_values(by='DateRep', ascending=False)
    dates = df['DateRep']
    return {'first': datetime.strptime(dates.iloc[-1], '%Y-%m-%d').strftime('%d-%m-%Y'), 'last': datetime.strptime(dates.iloc[0], '%Y-%m-%d').strftime('%d-%m-%Y')}

def get_total_cases(df):#
    return df['NewConfCases'].sum()

def get_total_deaths(df):#
    return df['NewDeaths'].sum()

def get_total_casesEU(df):#
    df = df[df['EU']=='EU']
    return df['NewConfCases'].sum()

def get_total_deathsEU(df):#
    df = df[df['EU']=='EU']
    return df['NewDeaths'].sum()

def get_total_cases_nonEU(df):
    df = df[df['EU']!='EU']
    return df['NewConfCases'].sum()

def get_total_deaths_nonEU(df):#
    df = df[df['EU']!='EU']
    return df['NewDeaths'].sum()

def get_todays_cases_EU(df):
    df=df[df['EU']=='EU']
    df1 = df.groupby('DateRep')['NewConfCases'].sum().reset_index()
    df1 = df1.sort_values(by='DateRep')
    return df1['NewConfCases'].iloc[-1]

def get_todays_cases_nonEU(df):
    df=df[df['EU']!='EU']
    df1 = df.groupby('DateRep')['NewConfCases'].sum().reset_index()
    df1 = df1.sort_values(by='DateRep')
    return df1['NewConfCases'].iloc[-1]

def get_todays_cases_global(df):
    df1 = df.groupby('DateRep')['NewConfCases'].sum().reset_index()
    df1 = df1.sort_values(by='DateRep')
    return df1['NewConfCases'].iloc[-1]

def get_todays_deaths_EU(df):
    df=df[df['EU']=='EU']
    df1 = df.groupby('DateRep')['NewDeaths'].sum().reset_index()
    df1 = df1.sort_values(by='DateRep')
    return df1['NewDeaths'].iloc[-1]

def get_todays_deaths_nonEU(df):
    df=df[df['EU']!='EU']
    df1 = df.groupby('DateRep')['NewDeaths'].sum().reset_index()
    df1 = df1.sort_values(by='DateRep')
    return df1['NewDeaths'].iloc[-1]

def get_todays_deaths_global(df):
    df1 = df.groupby('DateRep')['NewDeaths'].sum().reset_index()
    df1 = df1.sort_values(by='DateRep')
    return df1['NewDeaths'].iloc[-1]

def get_total_cases_per_day(df):#
    df1 = df.groupby('DateRep')['NewConfCases'].sum().reset_index()
    return df1

def get_total_deaths_per_day(df):
    df1 = df.groupby('DateRep')['NewDeaths'].sum().reset_index()
    return df1

def get_total_cases_per_country_per_day(df):#
    df1 = df.groupby(['DateRep','CountryExp'])['NewConfCases'].sum().reset_index()
    return df1

def get_total_deaths_per_country_per_day(df):#
    df1 = df.groupby(['DateRep', 'CountryExp'])['NewDeaths'].sum().reset_index()
    return df1

def get_total_cases_per_country(df):
    df1 = df.groupby('CountryExp')['NewConfCases'].sum().reset_index()
    return df1

def get_total_cases_per_country_EU(df):
    df1 = df[df['EU']=='EU']
    df1 = df.groupby('CountryExp')['NewConfCases'].sum().reset_index()
    return df1

def get_total_cases_per_country_nonEU(df):
    df1 = df[df['EU']!='EU']
    df1 = df.groupby('CountryExp')['NewConfCases'].sum().reset_index()
    return df1

def get_total_cases_per_country_hf(df):
    df1 = df.groupby(['CountryExp','hf_score'])['NewConfCases'].sum().reset_index()
    return df1

def get_total_cases_per_country_cap(df):
    df1 = df.groupby(['CountryExp','Corruption'])['NewConfCases'].sum().reset_index()
    return df1

def get_total_deaths_per_country(df):
    df1 = df.groupby('CountryExp')['NewDeaths'].sum().reset_index()
    return df1

def get_total_deaths_per_country_EU(df):
    df1 = df[df['EU']=='EU']
    df1 = df.groupby('CountryExp')['NewDeaths'].sum().reset_index()
    return df1

def get_total_deaths_per_country_nonEU(df):
    df1 = df[df['EU']!='EU']
    df1 = df.groupby('CountryExp')['NewDeaths'].sum().reset_index()
    return df1

def get_cases_per_specific_country(df,country):
    df1 = df[df['CountryExp']==country]
    df2 = df1.groupby(['DateRep','CountryExp'])['NewConfCases'].sum().reset_index()
    return df2

def get_deaths_per_specific_country(df,country):
    df1 = df[df['CountryExp']==country]
    df2 = df1.groupby(['DateRep','CountryExp'])['NewDeaths'].sum().reset_index()
    return df2

def get_total_distribution_of_cases(df):
    dfa = get_total_cases_per_country(df)
    # print (dfa)
    val = 'NewConfCases'
    stats_df = dfa \
        .groupby(val) \
        [val] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns={val: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()

    # CCDF
    stats_df['ccdf'] = 1 - stats_df['cdf']

    # ODDS
    stats_df['odds'] = stats_df['cdf'] / stats_df['ccdf']
    stats_df = stats_df.reset_index()
    return stats_df

def get_total_distribution_of_cases_per_specific_country(df,country):
    dfa = get_cases_per_specific_country(df,country)
    # print (dfa)
    val = 'NewConfCases'
    stats_df = dfa \
        .groupby(val) \
        [val] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns={val: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()

    # CCDF
    stats_df['ccdf'] = 1 - stats_df['cdf']

    # ODDS
    stats_df['odds'] = stats_df['cdf'] / stats_df['ccdf']
    stats_df = stats_df.reset_index()
    return stats_df

def get_total_distribution_of_deaths(df):
    dfa = get_total_deaths_per_country(df)
    # print (dfa)
    val = 'NewDeaths'
    stats_df = dfa \
        .groupby(val) \
        [val] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns={val: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()

    # CCDF
    stats_df['ccdf'] = 1 - stats_df['cdf']

    # ODDS
    stats_df['odds'] = stats_df['cdf'] / stats_df['ccdf']
    stats_df = stats_df.reset_index()
    return stats_df

def get_total_distribution_of_deaths_per_specific_country(df,country):
    dfa = get_deaths_per_specific_country(df,country)
    # print (dfa)
    val = 'NewDeaths'
    stats_df = dfa \
        .groupby(val) \
        [val] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns={val: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()

    # CCDF
    stats_df['ccdf'] = 1 - stats_df['cdf']

    # ODDS
    stats_df['odds'] = stats_df['cdf'] / stats_df['ccdf']
    stats_df = stats_df.reset_index()
    return stats_df

def get_cases_per_capita(df):
    df1 = df.groupby('Log of GDP per capita')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_life_expectancy(df):
    df1 = df.groupby('Healthy life expectancy')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_generosity(df):
    df1 = df.groupby('Generosity')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_social_support(df):
    df1 = df.groupby('Social support')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_corruption(df):
    df1 = df.groupby('Corruption')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_freedom(df):
    df1 = df.groupby('Freedom')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_human_freedom(df):
    # print (df['hf_score'],df['NewConfCases'])
    # df['NewConfCases']+=1
    # df['NewConfCases']=df['NewConfCases'].apply(np.log10)
    df1 = df.groupby('hf_score')['NewConfCases'].sum().reset_index()
    return df1

def get_cases_per_rank(df):
    df1 = df.groupby('Ladder')['NewConfCases'].sum().reset_index()
    return df1

def get_countries_per_capita(df):
    df = df[df['Log of GDP per capita']>-1]
    df1 = df.groupby('CountryExp')['Log of GDP per capita'].mean().to_frame('capita').reset_index()
    return df1

def get_recovered_cases_in_greece():
    data = requests.get("https://covid19.mathdro.id/api/countries/Greece/recovered").json()
    return data[0]['recovered']

def get_mapped_data(df):
    df1 = df.groupby(['CountryExp','lat','lon'])['NewDeaths','NewConfCases'].sum().reset_index()
    return df1

def map_greek_data():
    import pandas as pd
    from geopy.geocoders import Nominatim
    import pickle
    grcases = pd.read_csv('static/data/Greece.csv')
    locs = grcases['cities'].tolist()
    geolocator = Nominatim(user_agent="COVID")
    mapping={}
    for l in locs:
        try:
            location = geolocator.geocode(l)
            print (l)
            mapping[l]=(location.latitude, location.longitude)
        except:
            print ('none')
    maps = pickle.dump(mapping,open('mappingGR','wb'))

def get_greek_data():
    mapping = pickle.load(open('static/data/mappingGR','rb'))
    df = pd.read_csv('static/data/Greece.csv')
    latdict={}
    londict={}
    for k,v in mapping.items():
        latdict[k]=round(v[0],3)
        londict[k]=round(v[1],3)
    df['lat']=df['cities'].map(latdict)
    df['lon']=df['cities'].map(londict)
    return (df)

# print (get_greek_data())
# from collections import Counter

# df =df.dropna()
# print (set(df['CountryExp']))
# print (get_total_distribution_of_deaths(df))
# # print (len(set(sorted(df['CountryExp'].tolist()))))
# print (Counter(df['CountryExp'].tolist()))
# print (get_countries_per_capita(df))
# print (get_todays_cases_EU(df))
# # print (type(get_todays_cases_EU(df)))
# print (get_todays_cases_nonEU(df))
# # print (type(get_todays_cases_nonEU(df)))
# df1 = get_total_cases_per_country_hf(df)
# # print (df1)
# print (df1[df1['CountryExp']=='Greece'])