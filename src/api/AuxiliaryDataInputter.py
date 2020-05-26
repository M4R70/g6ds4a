import pandas as pd
import math
from scipy.spatial import cKDTree
import geopandas as gpd
import numpy as np


class AuxiliaryDataInputter:
    def __init__(self):
        data_dir = "./data"
        # load csv
        bus_df = gpd.read_file(data_dir + "/paradas-de-colectivo.geojson")
        metro_df = pd.read_csv(data_dir + "/estaciones-de-subte.csv")
        bike_df = pd.read_csv(data_dir + "/nuevas-estaciones-bicicletas-publicas.csv")
        train_df = pd.read_csv(data_dir + "/estaciones-de-ferrocarril.csv")
        highway_access_df = pd.read_csv(data_dir + "/peajes-y-porticos-autopistas.csv")
        garages_df = pd.read_csv(data_dir + "/garajes-comerciales.csv")
        crime_df = pd.read_csv(data_dir + "/Delitos.csv")
        cinema_df = pd.read_csv(data_dir + "/Cines.csv")
        theatre_df = pd.read_csv(data_dir + "/Teatros.csv")
        taxi_df = pd.read_csv(data_dir + "/paradas-de-taxis.csv")
        education_df = pd.read_csv(data_dir + "/establecimientos-educativos.csv")

        # column name consistency
        bus_df['lat'] = bus_df['stop_lat']
        bus_df['long'] = bus_df['stop_lon']

        cinema_df['lat'] = cinema_df['latitud']
        cinema_df['long'] = cinema_df['longitud']

        theatre_df['lat'] = cinema_df['latitud']
        theatre_df['long'] = cinema_df['longitud']

        self.dataframes = {'bus': bus_df ,
                           'metro': metro_df ,
                           'bike': bike_df ,
                           'train': train_df ,
                           'garages': garages_df ,
                           'highway_access': highway_access_df ,
                           'crime': crime_df ,
                           'cinema': cinema_df ,
                           'theatre': theatre_df ,
                           'taxi': taxi_df ,
                           'education': education_df
                           }
        self.features = ['lat' ,
                         'lon' ,
                         'rooms' ,
                         'bedrooms' ,
                         'bathrooms' ,
                         'surface_total' ,
                         'surface_covered' ,
                         'bus_in_100_m' ,
                         'bus_in_250_m' ,
                         'bus_in_500_m' ,
                         'bus_in_1000_m' ,
                         'bus_in_2500_m' ,
                         'metro_in_100_m' ,
                         'metro_in_250_m' ,
                         'metro_in_500_m' ,
                         'metro_in_1000_m' ,
                         'metro_in_2500_m' ,
                         'bike_in_100_m' ,
                         'bike_in_250_m' ,
                         'bike_in_500_m' ,
                         'bike_in_1000_m' ,
                         'bike_in_2500_m' ,
                         'train_in_100_m' ,
                         'train_in_250_m' ,
                         'train_in_500_m' ,
                         'train_in_1000_m' ,
                         'train_in_2500_m' ,
                         'garages_in_100_m' ,
                         'garages_in_250_m' ,
                         'garages_in_500_m' ,
                         'garages_in_1000_m' ,
                         'garages_in_2500_m' ,
                         'highway_access_in_100_m' ,
                         'highway_access_in_250_m' ,
                         'highway_access_in_500_m' ,
                         'highway_access_in_1000_m' ,
                         'highway_access_in_2500_m' ,
                         'crime_in_100_m' ,
                         'crime_in_250_m' ,
                         'crime_in_500_m' ,
                         'crime_in_1000_m' ,
                         'crime_in_2500_m' ,
                         'cinema_in_100_m' ,
                         'cinema_in_250_m' ,
                         'cinema_in_500_m' ,
                         'cinema_in_1000_m' ,
                         'cinema_in_2500_m' ,
                         'theatre_in_100_m' ,
                         'theatre_in_250_m' ,
                         'theatre_in_500_m' ,
                         'theatre_in_1000_m' ,
                         'theatre_in_2500_m' ,
                         'taxi_in_100_m' ,
                         'taxi_in_250_m' ,
                         'taxi_in_500_m' ,
                         'taxi_in_1000_m' ,
                         'taxi_in_2500_m' ,
                         'education_in_100_m' ,
                         'education_in_250_m' ,
                         'education_in_500_m' ,
                         'education_in_1000_m' ,
                         'education_in_2500_m' ,
                         'monoambiente' ,
                         'apto_profesional' ,
                         'cochera' ,
                         'torre' ,
                         'studio' ,
                         'amenities' ,
                         'pileta' ,
                         'sum' ,
                         'gym' ,
                         'laundry' ,
                         'balcon' ,
                         'losa_radiante' ,
                         'amoblado' ,
                         'parrilla' ,
                         'duplex' ,
                         'propiedad_horizontal' ,
                         'usd_market' ,
                         'usd_oficial' ,
                         'nearest_bus' ,
                         'nearest_metro' ,
                         'nearest_bike' ,
                         'nearest_train' ,
                         'nearest_garages' ,
                         'nearest_highway_access' ,
                         'nearest_crime' ,
                         'nearest_cinema' ,
                         'nearest_taxi' ,
                         'nearest_education' ,
                         'neighborhood_Abasto' ,
                         'neighborhood_Agronomía' ,
                         'neighborhood_Almagro' ,
                         'neighborhood_Balvanera' ,
                         'neighborhood_Barracas' ,
                         'neighborhood_Barrio Norte' ,
                         'neighborhood_Belgrano' ,
                         'neighborhood_Boca' ,
                         'neighborhood_Boedo' ,
                         'neighborhood_Caballito' ,
                         'neighborhood_Catalinas' ,
                         'neighborhood_Centro / Microcentro' ,
                         'neighborhood_Chacarita' ,
                         'neighborhood_Coghlan' ,
                         'neighborhood_Colegiales' ,
                         'neighborhood_Congreso' ,
                         'neighborhood_Constitución' ,
                         'neighborhood_Flores' ,
                         'neighborhood_Floresta' ,
                         'neighborhood_Las Cañitas' ,
                         'neighborhood_Liniers' ,
                         'neighborhood_Mataderos' ,
                         'neighborhood_Monserrat' ,
                         'neighborhood_Monte Castro' ,
                         'neighborhood_Nuñez' ,
                         'neighborhood_Once' ,
                         'neighborhood_Palermo' ,
                         'neighborhood_Parque Avellaneda' ,
                         'neighborhood_Parque Centenario' ,
                         'neighborhood_Parque Chacabuco' ,
                         'neighborhood_Parque Chas' ,
                         'neighborhood_Parque Patricios' ,
                         'neighborhood_Paternal' ,
                         'neighborhood_Pompeya' ,
                         'neighborhood_Puerto Madero' ,
                         'neighborhood_Recoleta' ,
                         'neighborhood_Retiro' ,
                         'neighborhood_Saavedra' ,
                         'neighborhood_San Cristobal' ,
                         'neighborhood_San Nicolás' ,
                         'neighborhood_San Telmo' ,
                         'neighborhood_Sin Determinar' ,
                         'neighborhood_Tribunales' ,
                         'neighborhood_Velez Sarsfield' ,
                         'neighborhood_Versalles' ,
                         'neighborhood_Villa Crespo' ,
                         'neighborhood_Villa Devoto' ,
                         'neighborhood_Villa General Mitre' ,
                         'neighborhood_Villa Lugano' ,
                         'neighborhood_Villa Luro' ,
                         'neighborhood_Villa Ortuzar' ,
                         'neighborhood_Villa Pueyrredón' ,
                         'neighborhood_Villa Real' ,
                         'neighborhood_Villa Riachuelo' ,
                         'neighborhood_Villa Santa Rita' ,
                         'neighborhood_Villa Soldati' ,
                         'neighborhood_Villa Urquiza' ,
                         'neighborhood_Villa del Parque' ,
                         'currency_ARS' ,
                         'currency_USD' ,
                         'property_type_Casa' ,
                         'property_type_Departamento' ,
                         'property_type_Local comercial' ,
                         'property_type_Oficina' ,
                         'property_type_PH' ,
                         'operation_type_Sale']

    def ohe(self,df):
        n = df['neighborhood'][0]

        dummy = "neighborhood_" + n
        # print(dummy)
        for f in self.features:
            if f == dummy:
                df[f] = 1
            elif f.startswith("neighborhood_"):
               df[f] = 0
            else:
                try:
                    a = df[f]
                except:
                   df[f] = 0
        return df

    def add_nearest(self,tdf):
        for name , df in self.dataframes.items():
            tree = create_kdTree(df)
            tdf = add_distance_to_nearest(tdf , name , tree)
        return tdf

    def add_radius(self,tdf):
        radiuses = [100 , 250 , 500 , 1000 , 2500]
        for name , df in self.dataframes.items():
            tree = create_kdTree(df)
            for r in radiuses:
                tdf = add_radius_column(tdf, name , tree , r)
                #column_name = f'{name}_in_{r}m'
                # print(column_name)
                # print(tdf[column_name][0])
                #
                # # print(f"{column_name} {self.res[column_name][0]}")



        return tdf

    def add_usd_pries(self,df):
        df['usd_market'] = 138
        df['usd_oficial'] = 70.32
        return df

    def add_aux_cols(self,df):
        df = self.ohe(df)
        df = self.add_radius(df)
        print('edu')
        print(df['education_in_2500_m'][0])
        df = self.add_nearest(df)
        df = self.add_usd_pries(df)
        return df


def add_usd_pries(row):
    row['usd_market'] = 138
    row['usd_oficial'] = 70.32


def coords_to_cartesian(coords):
    # asumes the earth is a perfect sphere with radius = 6371km
    lon , lat = coords
    lon = math.radians(lon)
    lat = math.radians(lat)

    R = 6371000  # radius of Earth in meters

    x = R * math.cos(lat) * math.cos(lon)
    y = R * math.cos(lat) * math.sin(lon)

    return (x , y)


def create_kdTree(df):
    # asumes df has a lat and long columns
    try:
        points = list(map(coords_to_cartesian , list(zip(df['long'] , df['lat']))))
    except KeyError:
        points = list(map(coords_to_cartesian , list(zip(df['lon'] , df['lat']))))
    return cKDTree(points)


def add_radius_column(target_df , name , tree , r):
    column_name = f'{name}_in_{r}m'
    target_df[column_name] = target_df.apply(
        lambda x: len(tree.query_ball_point(coords_to_cartesian((x['lon'] , x['lat'])) , r)) , axis=1)
    return target_df


def add_distance_to_nearest(target_df , name , tree):
    column_name = 'nearest_' + name
    target_df[column_name] = target_df.apply(lambda x: get_distance_to_nearest(tree , x) , axis=1)
    return target_df


def get_distance_to_nearest(tree , x):
    cartesian_point = coords_to_cartesian((x['lon'] , x['lat']))
    distance , indices = tree.query(cartesian_point , k=1)
    return distance

# def get_average_ppsm_radius(df, tree, x, r):
#     cartesian_point = coords_to_cartesian((x['lon'], x['lat']))
#     points_in_radius = tree.query_ball_point(cartesian_point, r)
#     ppsm_list = []
#     for p in points_in_radius:
#         point = tree.data[p]  # ??
#         point_df = df[(df['lon'] == point[0]) & (df['lat'] == point[1])]
#         point_df.apply(lambda x: ppsm_list.append(x['price_per_square_meter']))
#
#     if len(ppsm_list) == 0:
#         return 0
#     else:
#         return np.mean(ppsm_list)
#
#
# def add_average_ppsm_radius_column(target_df, tree, r):
#     column_name = f"ppsm_{r}_m"
#     target_df[column_name] = target_df.apply(lambda x: get_average_ppsm_radius(target_df, tree, x, r), axis=1)
