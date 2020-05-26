from joblib import load
import pandas as pd
from flask import Flask , request
from flask_cors import CORS
from flask_restful import Resource , Api
from bs4 import BeautifulSoup
import requests
import urllib
import json
from AuxiliaryDataInputter import AuxiliaryDataInputter

app = Flask(__name__)
cors = CORS(app , resources={r"*": {"origins": "*"}})
api = Api(app)


def geocode(addr , num):
    url = f"https://ws.usig.buenosaires.gob.ar/rest/normalizar_y_geocodificar_direcciones?calle={addr}&altura={num}&desambiguar=1"
    resp = requests.get(url)
    resp = resp.json()
    x = resp['GeoCodificacion']['x']
    y = resp['GeoCodificacion']['y']

    url2 = f"https://ws.usig.buenosaires.gob.ar/rest/convertir_coordenadas?x={x}&y={y}&output=lonlat"
    resp2 = requests.get(url2)
    resp2 = resp2.json()
    if resp2['tipo_resultado'] == "Ok":
        lon = float(resp2['resultado']['x'])
        lat = float(resp2['resultado']['y'])
    else:
        print('Failed to geocode x,y to lat lon')
        return 0 , 0

    return lat , lon


def separar_calle(s):
    l = s.split(' ')
    for x in l:
        try:
            n = x
        except ValueError:
            pass

    a = ' '.join([x for x in l if x != n])
    n = int(n)

    return a , n


class Model(Resource):
    def __init__(self , **kwargs):
        self.predictor = kwargs['predictor']
        self.inputter = kwargs['inputter']

        # this is horrible code formatting
        print('loaded')

    def get(self , data):
        # print('hola')
        data = json.loads(data)
        # print(data)
        print('\n \n \n \n')
        print('New request, attempting to geocode')
        address , altura = separar_calle(data['address'])

        lat , lon = geocode(address , altura)
        data['lat'] = lat
        data['lon'] = lon
        row = pd.DataFrame(data , index=[0])

        row = self.inputter.add_aux_cols(row)

        test = row[self.inputter.features].astype(float)

        #print(f"dict {dict(test)}")

        res = self.predictor.predict(test)

        final_price = int(round(res[0] * float(row['surface_total'][0])))

        final_price = '{:,}'.format(final_price)

        to_report = ['bus_in_500m' , 'metro_in_500m' , 'train_in_1000m' , 'education_in_2500m' , 'lat' , 'lon']

        response = {x: str(row[x][0]) for x in to_report}
        response['prediction'] = str(final_price)

        print(response)
        print('\n \n \n \n')
        return response


def get_df_and_features():
    df = pd.read_csv('ohe.csv')
    # df.drop(columns=['nearest_theatre'], inplace=True)
    df.drop(columns=['Unnamed: 0'] , inplace=True)
    features = [x for x in df.columns if
                x != 'target' and x != 'description' and x != 'id' and not x.startswith('price') and not x.startswith(
                    'price_in') and x != 'created_on']
    return features , df


if __name__ == '__main__':
    print('loading model...')
    predictor = load('model.joblib')
    # predictor = 2
    print('loading auxiliary data...')
    inputter = AuxiliaryDataInputter()
    # inputter = 3
    print('DONE! App running... \n \n \n')
    api.add_resource(Model , '/<data>' , resource_class_kwargs={'predictor': predictor , 'inputter': inputter})
    app.run(debug=False,host='0.0.0.0')
    # print('API ONLINE')
    # f, df = get_df_and_features()
    # print(api.predict(df[f].head(1)) - df['price_per_square_meter'].head(1))
