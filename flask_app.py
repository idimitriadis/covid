from flask import Flask, jsonify,render_template
from flask_restful import Resource, Api
import analysis
import pandas as pd
from flask_cors import CORS
import pickle


# df = analysis.merge_data()

app = Flask(__name__, template_folder='templates')
api = Api(app)
CORS(app)

# df1 = df.groupby('CountryExp')['NewConfCases'].sum().reset_index()
# df2 = df.groupby('CountryExp')['NewDeaths'].sum().reset_index()
# final_df = pd.merge(df1, df2, on='CountryExp')
# final_df.to_csv('static/table-data.csv', index=False)

@app.route('/')
def home():
    global df
    df = pickle.load(open('static/data/df.pickle', 'rb'))
    df1 = df.groupby('CountryExp')['NewConfCases'].sum().reset_index()
    df2 = df.groupby('CountryExp')['NewDeaths'].sum().reset_index()
    final_df = pd.merge(df1, df2, on='CountryExp')
    final_df.to_csv('static/data/table-data.csv', index=False)
    return render_template('index.html')


class getCountries(Resource):
    def get(self):
        result = list(set(df['CountryExp'].tolist()))
        result = sorted(result)
        return jsonify(result)

api.add_resource(getCountries, '/getCountries')

class totalCases(Resource):
    def get(self):
        from analysis import get_total_cases
        return (str(get_total_cases(df)))

api.add_resource(totalCases,'/totalCases')

class totalDeaths(Resource):
    def get(self):
        from analysis import get_total_deaths
        return (str(get_total_deaths(df)))

api.add_resource(totalDeaths,'/totalDeaths')

class totalCasesCountry(Resource):
    def get(self):
        from analysis import get_total_cases_per_country
        df1 = get_total_cases_per_country(df)
        mydict = dict(zip(df1['CountryExp'], df1['NewConfCases']))
        return (mydict)

api.add_resource(totalCasesCountry,'/totalCasesCountry')

class totalDeathsCountry(Resource):
    def get(self):
        from analysis import get_total_deaths_per_country
        df1 = get_total_deaths_per_country(df)
        mydict = dict(zip(df1['CountryExp'], df1['NewDeaths']))
        return (mydict)

api.add_resource(totalDeathsCountry,'/totalDeathsCountry')

class totalCasesDay(Resource):
    def get(self):
        from analysis import get_total_cases_per_day
        df1 = get_total_cases_per_day(df)
        df1['DateRep']= df1['DateRep'].astype(str)
        mydict = dict(zip(df1['DateRep'], df1['NewConfCases']))
        return (mydict)

api.add_resource(totalCasesDay,'/totalCasesDay')

class casesPerSpecificCountry(Resource):
    def get(self,country):
        from analysis import get_cases_per_specific_country
        df1 = get_cases_per_specific_country(df,country)
        df1['DateRep']= df1['DateRep'].astype(str)
        mydict = dict(zip(df1['DateRep'], df1['NewConfCases']))
        return (mydict)

api.add_resource(casesPerSpecificCountry,'/casesPerSpecificCountry/<string:country>')

class deathsPerSpecificCountry(Resource):
    def get(self,country):
        from analysis import get_deaths_per_specific_country
        df1 = get_deaths_per_specific_country(df,country)
        df1['DateRep']= df1['DateRep'].astype(str)
        mydict = dict(zip(df1['DateRep'], df1['NewDeaths']))
        return (mydict)

api.add_resource(deathsPerSpecificCountry,'/deathsPerSpecificCountry/<string:country>')

class totalDeathsDay(Resource):
    def get(self):
        from analysis import get_total_deaths_per_day
        df1 = get_total_deaths_per_day(df)
        df1['DateRep']= df1['DateRep'].astype(str)
        mydict = dict(zip(df1['DateRep'], df1['NewDeaths']))
        return (mydict)

api.add_resource(totalDeathsDay,'/totalDeathsDay')

class totalDays(Resource):
    def get(self):
        from analysis import get_dates
        mydict = get_dates(df)
        return (mydict)

api.add_resource(totalDays,'/totalDays')

class casesPerCapita(Resource):
    def get(self):
        from analysis import get_cases_per_capita
        df1 = get_cases_per_capita(df)
        mydict = dict(zip(df1['Log of GDP per capita'], df1['NewConfCases']))
        return (mydict)

api.add_resource(casesPerCapita,'/casesPerCapita')

class casesPerLifeExpectancy(Resource):
    def get(self):
        from analysis import get_cases_per_life_expectancy
        df1 = get_cases_per_life_expectancy(df)
        mydict = dict(zip(df1['Healthy life expectancy'], df1['NewConfCases']))
        return (mydict)

api.add_resource(casesPerLifeExpectancy,'/casesPerLifeExpectancy')


class totalCasesHumanFreedom(Resource):
    def get(self):
        from analysis import get_cases_per_human_freedom
        df1 = get_cases_per_human_freedom(df)
        df1 = df1[df1['hf_score'] >= 0]
        mydict = dict(zip(df1['hf_score'], df1['NewConfCases']))
        return (mydict)

api.add_resource(totalCasesHumanFreedom,'/totalCasesHumanFreedom')

class capitaPerCountry(Resource):
    def get(self):
        from analysis import get_countries_per_capita
        df1 = get_countries_per_capita(df)
        mydict = dict(zip(df1['CountryExp'],df1['capita']))
        return mydict

api.add_resource(capitaPerCountry,'/capitaPerCountry')

class casesCDF(Resource):
    def get(self):
        from analysis import get_total_distribution_of_cases
        df1 = get_total_distribution_of_cases(df)
        mydict = dict(zip(df1['NewConfCases'],df1['cdf']))
        return mydict

api.add_resource(casesCDF,'/casesCDF')

class casesPDF(Resource):
    def get(self):
        from analysis import get_total_distribution_of_cases
        df1 = get_total_distribution_of_cases(df)
        mydict = dict(zip(df1['NewConfCases'],df1['pdf']))
        return mydict

api.add_resource(casesPDF,'/casesPDF')

class casesODDS(Resource):
    def get(self):
        from analysis import get_total_distribution_of_cases
        df1 = get_total_distribution_of_cases(df)
        # df1 = df1.sort_values(by=['odds'],ascending=True)
        df1 = df1[0:df1.shape[0]-1]
        mydict = dict(zip(df1['NewConfCases'],df1['odds']))
        return mydict

api.add_resource(casesODDS,'/casesODDS')

class casesCountryCDF(Resource):
    def get(self,country):
        from analysis import get_total_distribution_of_cases_per_specific_country
        df1 = get_total_distribution_of_cases_per_specific_country(df,country)
        mydict = dict(zip(df1['NewConfCases'],df1['cdf']))
        return (mydict)

api.add_resource(casesCountryCDF,'/casesCountryCDF/<string:country>')

class casesCountryPDF(Resource):
    def get(self,country):
        from analysis import get_total_distribution_of_cases_per_specific_country
        df1 = get_total_distribution_of_cases_per_specific_country(df,country)
        mydict = dict(zip(df1['NewConfCases'],df1['pdf']))
        return (mydict)

api.add_resource(casesCountryPDF,'/casesCountryPDF/<string:country>')

class casesCountryODDS(Resource):
    def get(self,country):
        from analysis import get_total_distribution_of_cases_per_specific_country
        df1 = get_total_distribution_of_cases_per_specific_country(df,country)
        # df1 = df1.sort_values(by=['odds'],ascending=True)
        df1 = df1[0:df1.shape[0]-1]
        mydict = dict(zip(df1['NewConfCases'],df1['odds']))
        return (mydict)

api.add_resource(casesCountryODDS,'/casesCountryODDS/<string:country>')


class human_freedom(Resource):
    def get(self):
        from analysis import get_cases_per_human_freedom
        df1 = get_cases_per_human_freedom(df)
        mydict = dict(zip(df1['hf_score'],df1['NewConfCases']))
        return (mydict)

api.add_resource(human_freedom,'/human_freedom')

class human_freedom_per_country(Resource):
    def get(self):
        from analysis import get_total_cases_per_country_hf
        df1 = get_total_cases_per_country_hf(df)
        df1 = df1.sort_values(by=['hf_score'],ascending=True)
        mydict = dict(zip(df1['CountryExp'],zip(df1['NewConfCases'],df1['hf_score'])))
        return (mydict)

api.add_resource(human_freedom_per_country,'/human_freedom_per_country')


class china_vs_EU(Resource):
    def get(self):
        from analysis import get_total_cases_per_country_per_day,get_total_cases_per_countryEU_per_day
        newdf = df
        df1 = get_total_cases_per_country_per_day(newdf)
        df2 = get_total_cases_per_countryEU_per_day(newdf)
        dfCN=df1[df1['CountryExp']=='China']
        dfCN=dfCN.rename(columns={"NewConfCases": "NewConfCasesCN"})
        dfEU=df2[df2['EU']=='EU']
        compare = pd.merge(dfCN,dfEU,on='DateRep')
        compare = compare[20:]
        compare['DateRep']= compare['DateRep'].astype(str)
        mydict = dict(zip(compare['DateRep'],zip(compare['NewConfCases'],compare['NewConfCasesCN'])))
        return (mydict)

api.add_resource(china_vs_EU,'/china_vs_EU')


class capita_and_cases_per_country(Resource):
    def get(self):
        from analysis import get_total_cases_per_country_cap
        df1 = get_total_cases_per_country_cap(df)
        df1 = df1[df1['Corruption']>0]
        df1 = df1.sort_values(by=['Corruption'],ascending=True)
        mydict = dict(zip(df1['CountryExp'],zip(df1['NewConfCases'],df1['Corruption'])))
        return (mydict)

api.add_resource(capita_and_cases_per_country,'/capita_and_cases_per_country')

class casesEU(Resource):
    def get(self):
        from analysis import get_total_casesEU
        df1 = get_total_casesEU(df)
        return (int(df1))

api.add_resource(casesEU,'/casesEU')

class casesnonEU(Resource):
    def get(self):
        from analysis import get_total_cases_nonEU
        df1 = get_total_cases_nonEU(df)
        return (int(df1))

api.add_resource(casesnonEU,'/casesnonEU')

class deathsEU(Resource):
    def get(self):
        from analysis import get_total_deathsEU
        df1 = get_total_deathsEU(df)
        return (int(df1))

api.add_resource(deathsEU,'/deathsEU')

class deathsnonEU(Resource):
    def get(self):
        from analysis import get_total_deaths_nonEU
        df1 = get_total_deaths_nonEU(df)
        return (int(df1))

api.add_resource(deathsnonEU,'/deathsnonEU')

class cases_todayEU(Resource):
    def get(self):
        from analysis import get_todays_cases_EU
        df1 = get_todays_cases_EU(df)
        return (int(df1))

api.add_resource(cases_todayEU,'/cases_todayEU')

class cases_today_nonEU(Resource):
    def get(self):
        from analysis import get_todays_cases_nonEU
        df1 = get_todays_cases_nonEU(df)
        return (int(df1))

api.add_resource(cases_today_nonEU,'/cases_today_nonEU')

class cases_today_global(Resource):
    def get(self):
        from analysis import get_todays_cases_global
        df1 = get_todays_cases_global(df)
        return (int(df1))

api.add_resource(cases_today_global,'/cases_today_global')

class deaths_today_EU(Resource):
    def get(self):
        from analysis import get_todays_deaths_EU
        df1 = get_todays_deaths_EU(df)
        return (int(df1))

api.add_resource(deaths_today_EU,'/deaths_today_EU')

class deaths_today_nonEU(Resource):
    def get(self):
        from analysis import get_todays_deaths_nonEU
        df1 = get_todays_deaths_nonEU(df)
        return (int(df1))

api.add_resource(deaths_today_nonEU,'/deaths_today_nonEU')

class deaths_today_global(Resource):
    def get(self):
        from analysis import get_todays_deaths_global
        df1 = get_todays_deaths_global(df)
        return (int(df1))

api.add_resource(deaths_today_global,'/deaths_today_global')

class recovered_greece(Resource):
    def get(self):
        from analysis import get_recovered_cases_in_greece
        return (int(get_recovered_cases_in_greece()))

api.add_resource(recovered_greece,'/recovered_greece')

class mapped_results(Resource):
    def get(self):
        from analysis import get_mapped_data
        # mydict = dict(zip(df['CountryExp'],zip(df['NewDeaths'],df['NewConfCases'])))
        # return jsonify(mydict)
        df1 = get_mapped_data(df)
        mydict={}
        for i,r in df1.iterrows():
            mydict.update({r['CountryExp']:[r['lat'],r['lon'],r['NewDeaths'],r['NewConfCases']]})
        return jsonify(mydict)

api.add_resource(mapped_results,'/mapped_results')

class greek_data(Resource):
    def get(self):
        from analysis import get_greek_data
        df1 = get_greek_data()
        mydict={}
        for i,r in df1.iterrows():
            mydict.update({r['cities']:[r['cases'],r['deaths'],r['lat'],r['lon']]})
        return jsonify(mydict)

api.add_resource(greek_data,'/greek_data')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
