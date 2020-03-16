from flask import Flask
from flask_restful import Resource, Api
import analysis
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

class totalCases(Resource):
    def get(self):
        from analysis import merge_data,get_total_cases
        df = merge_data()
        return (str(get_total_cases(df)))

api.add_resource(totalCases,'/totalCases')

class totalDeaths(Resource):
    def get(self):
        from analysis import merge_data,get_total_deaths
        df = merge_data()
        return (str(get_total_deaths(df)))

api.add_resource(totalDeaths,'/totalDeaths')

class totalCasesCountry(Resource):
    def get(self):
        from analysis import merge_data,get_total_cases_per_country
        df = merge_data()
        df1 = get_total_cases_per_country(df)
        mydict = dict(zip(df1['CountryExp'], df1['NewConfCases']))
        return (mydict)

api.add_resource(totalCasesCountry,'/totalCasesCountry')

class totalDeathsCountry(Resource):
    def get(self):
        from analysis import merge_data,get_total_deaths_per_country
        df = merge_data()
        df1 = get_total_deaths_per_country(df)
        mydict = dict(zip(df1['CountryExp'], df1['NewDeaths']))
        return (mydict)

api.add_resource(totalDeathsCountry,'/totalDeathsCountry')

class totalCasesDay(Resource):
    def get(self):
        from analysis import merge_data,get_total_cases_per_day
        df = merge_data()
        df1 = get_total_cases_per_day(df)
        df1['DateRep']= df1['DateRep'].astype(str)
        mydict = dict(zip(df1['DateRep'], df1['NewConfCases']))
        return (mydict)

api.add_resource(totalCasesDay,'/totalCasesDay')

class casesPerSpecificCountry(Resource):
    def get(self,country):
        country = country.upper()
        from analysis import merge_data,get_cases_per_specific_country
        df = merge_data()
        df1 = get_cases_per_specific_country(df,country)
        df1['DateRep']= df1['DateRep'].astype(str)
        mydict = dict(zip(df1['DateRep'], df1['NewConfCases']))
        return (mydict)

api.add_resource(casesPerSpecificCountry,'/casesPerSpecificCountry/<string:country>')

class deathsPerSpecificCountry(Resource):
    def get(self,country):
        country = country.upper()
        from analysis import merge_data, get_deaths_per_specific_country
        df = merge_data()
        df1 = get_deaths_per_specific_country(df,country)
        df1['DateRep']= df1['DateRep'].astype(str)
        mydict = dict(zip(df1['DateRep'], df1['NewDeaths']))
        return (mydict)

api.add_resource(deathsPerSpecificCountry,'/deathsPerSpecificCountry/<string:country>')

class totalDeathsDay(Resource):
    def get(self):
        from analysis import merge_data,get_total_deaths_per_day
        df = merge_data()
        df1 = get_total_deaths_per_day(df)
        df1['DateRep']= df1['DateRep'].astype(str)
        mydict = dict(zip(df1['DateRep'], df1['NewDeaths']))
        return (mydict)

api.add_resource(totalDeathsDay,'/totalDeathsDay')

class totalDays(Resource):
    def get(self):
        from analysis import merge_data,get_dates
        df = merge_data()
        mydict = get_dates(df)
        return (mydict)

api.add_resource(totalDays,'/totalDays')

class casesPerCapita(Resource):
    def get(self):
        from analysis import merge_data, get_cases_per_capita
        df = merge_data()
        df1 = get_cases_per_capita(df)
        mydict = dict(zip(df1['Log of GDP per capita'], df1['NewConfCases']))
        return (mydict)

api.add_resource(casesPerCapita,'/casesPerCapita')

class casesPerLifeExpectancy(Resource):
    def get(self):
        from analysis import merge_data, get_cases_per_life_expectancy
        df = merge_data()
        df1 = get_cases_per_life_expectancy(df)
        mydict = dict(zip(df1['Healthy life expectancy'], df1['NewConfCases']))
        return (mydict)

api.add_resource(casesPerLifeExpectancy,'/casesPerLifeExpectancy')


class totalCasesHumanFreedom(Resource):
    def get(self):
        from analysis import merge_data,get_cases_per_human_freedom
        df = merge_data()
        df1 = get_cases_per_human_freedom(df)
        df1 = df1[df1['hf_score'] >= 0]
        mydict = dict(zip(df1['hf_score'], df1['NewConfCases']))
        return (mydict)

api.add_resource(totalCasesHumanFreedom,'/totalCasesHumanFreedom')

class capitaPerCountry(Resource):
    def get(self):
        from analysis import merge_data,get_countries_per_capita
        df = merge_data()
        df1 = get_countries_per_capita(df)
        mydict = dict(zip(df1['CountryExp'],df1['capita']))
        return mydict

api.add_resource(capitaPerCountry,'/capitaPerCountry')

class casesCDF(Resource):
    def get(self):
        from analysis import merge_data,get_total_distribution_of_cases
        df = merge_data()
        df1 = get_total_distribution_of_cases(df)
        mydict = dict(zip(df1['NewConfCases'],df1['cdf']))
        return mydict

api.add_resource(casesCDF,'/casesCDF')

class casesPDF(Resource):
    def get(self):
        from analysis import merge_data,get_total_distribution_of_cases
        df = merge_data()
        df1 = get_total_distribution_of_cases(df)
        mydict = dict(zip(df1['NewConfCases'],df1['pdf']))
        return mydict

api.add_resource(casesPDF,'/casesPDF')

class casesODDS(Resource):
    def get(self):
        from analysis import merge_data,get_total_distribution_of_cases
        df = merge_data()
        df1 = get_total_distribution_of_cases(df)
        df1 = df1.sort_values(by=['odds'],ascending=True)
        df1 = df1[0:df1.shape[0]-2]
        mydict = dict(zip(df1['NewConfCases'],df1['odds']))
        return mydict

api.add_resource(casesODDS,'/casesODDS')

class casesCountryCDF(Resource):
    def get(self,country):
        country = country.upper()
        from analysis import merge_data, get_total_distribution_of_cases_per_specific_country
        df = merge_data()
        df1 = get_total_distribution_of_cases_per_specific_country(df,country)
        mydict = dict(zip(df1['NewConfCases'],df1['cdf']))
        return (mydict)

api.add_resource(casesCountryCDF,'/casesCountryCDF/<string:country>')

class casesCountryPDF(Resource):
    def get(self,country):
        country = country.upper()
        from analysis import merge_data, get_total_distribution_of_cases_per_specific_country
        df = merge_data()
        df1 = get_total_distribution_of_cases_per_specific_country(df,country)
        mydict = dict(zip(df1['NewConfCases'],df1['pdf']))
        return (mydict)

api.add_resource(casesCountryPDF,'/casesCountryPDF/<string:country>')

class casesCountryODDS(Resource):
    def get(self,country):
        country = country.upper()
        from analysis import merge_data, get_total_distribution_of_cases_per_specific_country
        df = merge_data()
        df1 = get_total_distribution_of_cases_per_specific_country(df,country)
        df1 = df1.sort_values(by=['odds'],ascending=True)
        df1 = df1[0:df1.shape[0]-2]
        mydict = dict(zip(df1['NewConfCases'],df1['odds']))
        return (mydict)

api.add_resource(casesCountryODDS,'/casesCountryODDS/<string:country>')


class human_freedom(Resource):
    def get(self):
        from analysis import merge_data, get_cases_per_human_freedom
        df = merge_data()
        df1 = get_cases_per_human_freedom(df)
        mydict = dict(zip(df1['hf_score'],df1['NewConfCases']))
        return (mydict)

api.add_resource(human_freedom,'/human_freedom')

class human_freedom_per_country(Resource):
    def get(self):
        from analysis import merge_data, get_total_cases_per_country_hf
        df = merge_data()
        df1 = get_total_cases_per_country_hf(df)
        df1['wanted'] = df1['NewConfCases']+df1['CountryExp']
        mydict = dict(zip(df1['hf_score'],df['wanted']))
        return (mydict)

api.add_resource(human_freedom_per_country,'/human_freedom_per_country')


app.run(port=5000)
