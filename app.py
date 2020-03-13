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

class totalCasesDay(Resource):
    def get(self):
        from analysis import merge_data,get_total_cases_per_day
        df = merge_data()
        df1 = get_total_cases_per_day(df)
        df1['DateRep']= df1['DateRep'].astype(str)
        mydict = dict(zip(df1['DateRep'], df1['NewConfCases']))
        return (mydict)

api.add_resource(totalCasesDay,'/totalCasesDay')



app.run(port=5000)
