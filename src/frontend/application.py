import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input , Output , State
import requests
from dash.exceptions import PreventUpdate
import traceback
import sys
import urllib.parse
import json

neighborhoods = ['Abasto' , 'Agronomía' , 'Almagro' , 'Balvanera' , 'Barracas' , 'Barrio Norte' , 'Belgrano' , 'Boca' ,
                 'Boedo' , 'Caballito' , 'Catalinas' , 'Centro / Microcentro' , 'Chacarita' , 'Coghlan' , 'Colegiales' ,
                 'Congreso' , 'Constitución' , 'Flores' , 'Floresta' , 'Las Cañitas' , 'Liniers' , 'Mataderos' ,
                 'Monserrat' , 'Monte Castro' , 'Nuñez' , 'Once' , 'Palermo' , 'Parque Avellaneda' ,
                 'Parque Centenario' , 'Parque Chacabuco' , 'Parque Chas' , 'Parque Patricios' , 'Paternal' ,
                 'Pompeya' , 'Puerto Madero' , 'Recoleta' , 'Retiro' , 'Saavedra' , 'San Cristobal' , 'San Nicolás' ,
                 'San Telmo' , 'Velez Sarsfield' , 'Versalles' , 'Villa Crespo' , 'Villa Devoto' ,
                 'Villa General Mitre' , 'Villa Lugano' , 'Villa Luro' , 'Villa Ortuzar' , 'Villa Pueyrredón' ,
                 'Villa Real' , 'Villa Riachuelo' , 'Villa Santa Rita' , 'Villa Soldati' , 'Villa Urquiza' ,
                 'Villa del Parque']
property_types = ['Casa' , 'Departamento' , 'Local comercial' , 'Oficina' , 'PH']


def data_list_children(l):
    return [html.Option(value=word) for word in l]


def option_list(l):
    if l == []: return []
    return [{'label': x , 'value': x} for x in l]


def normalizar(calle , n):
    url = 'https://ws.usig.buenosaires.gob.ar/rest/normalizar_y_geocodificar_direcciones?calle=' + str(
        calle) + '&altura=' + str(n) + '&desambiguar=0'
    resp = requests.get(url)
    resp = resp.json()
    try:
        res = [x['Calle'] + ' ' + x['Altura'] for x in resp['Normalizacion']['DireccionesCalleAltura']['direcciones']]
    except KeyError:
        #print(resp)
        return {}

    return res


extras = [
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
]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__ , external_stylesheets=external_stylesheets)
application = app.server
app.scripts.config.serve_locally = True

default_suggestions = ['def suggestion']

item_style = {
    "display": 'inline-block' ,
    "verticalAlign": "middle" ,
}

app.layout = html.Div(
    style={
        "display": 'flex' ,
        'flexDirection': "column" ,
        'alignItems': 'center' ,
    } ,
    children=[

        html.Div(children=[
            html.Div(id='placeholder' , style={'display': 'none'}) ,

            html.H1(children='Real Estate Price Estimation') ,

            html.Div(children=''' #DS4A Team 6 Practicum Project.''' , style={'paddingBottom': '20px'}) ,
        ],style={'text-align':'center'}),

        html.Div(children=[

            html.Div(id='form' , children=[
                dcc.Dropdown(
                    id='address' ,
                    options=[] ,
                    placeholder="Street Name and #" ,
                    style=item_style ,
                ) ,
                dcc.Dropdown(
                    id='neighborhood' ,
                    options=option_list(neighborhoods) ,
                    placeholder="Neighborhood" ,
                    style=item_style ,
                ) ,
                dcc.Dropdown(
                    id='property_type' ,
                    options=option_list(property_types) ,
                    placeholder="Property Type" ,
                    style=item_style ,
                ) ,
                dcc.Input(id="rooms" , type="number" , placeholder="# of Rooms" , style=item_style) ,
                dcc.Input(id="bathrooms" , type="number" , placeholder="# of Bathrooms" , style=item_style) ,
                dcc.Input(id="bedrooms" , type="number" , placeholder="# of Bedrooms" , style=item_style) ,
                dcc.Input(id="surface_total" , type="number" , placeholder="Surface Total (m^2)" , style=item_style) ,
                dcc.Input(id="surface_covered" , type="number" , placeholder="Surface Covered (m^2)" , style=item_style) ,
                dcc.Dropdown(
                    id='keywords' ,
                    options=option_list(extras) ,
                    style=item_style ,
                    multi=True ,
                    placeholder='keywords (optional)'
                ) ,

                html.Button('Submit' , id='submit-button' , n_clicks=0 , style=item_style , value='hola') ,



            ] ,
                     style={  # style for the form
                         "display": 'flex',
                         'flexDirection': "column",
                         'width': '50%',
                         # 'align-items':'',
                         'padding':'25px'
                     }) ,

            html.Div(id='res_div' , children=[
                html.H2(id='resh1' , children='Results:' , style={'display': 'none'}) ,
                html.H4(id='resh3' , children='hola \n test \n test' , style={'display': 'none'}) ,
            ],style={'padding':'25px'})
        ],style={"display": 'flex','flexDirection': "row",'justifyContent':'space-around','width':'50%'})

    ])


#

@app.callback(
    Output('res_div' , 'children') ,
    [Input('submit-button' , 'n_clicks') , Input('form' , 'children')])
def submit(n_clicks , form):
    if n_clicks == 0:
        raise PreventUpdate

    try:
        data = {x['props']['id']: x['props']['value'] for x in form if
                x['props']['id'] not in ['submit-button' , 'keywords' , 'res_div']}
        for x in form:
            item = x['props']['id']
            if item == 'keywords':
                if 'value' in x['props']:
                    values = x['props']['value']
                    for y in extras:
                        if y in values:
                            data[y] = 1
                        else:
                            data[y] = 0

        #print(data)
    except KeyError:
        print(traceback.format_exc())

    encoded_data = urllib.parse.quote(json.dumps(data))

    resp = requests.get('http://ec2-52-15-217-248.us-east-2.compute.amazonaws.com:5000/' + encoded_data)

    resp = resp.json()
    print(resp)

    res = [
            html.H4(id='pred' , children=f"Estimated Price: {resp['prediction']}" , style={'display': 'block'}) ,
            html.H4(id='results', children=f"Additional Data:", style={'display': 'block'}),
    ]

    for k,v in resp.items():
        new = html.H5(id=f'{k}', children=f"{k} = {v}", style={'display': 'block'})
        res.append(new)
    return res


# @app.callback(
#     Output('placeholder' , 'style') ,
#     [Input('submit-button' , 'n_clicks') , Input('form' , 'children')])

# @app.callback(
#     Output('dropdown_div', 'style'),
#     [Input('submit-val', 'n_clicks')])
# def update_output(n_clicks):
#     #print('asd')
#     if n_clicks%2 == 0:
#         return {'display': 'block'}
#     else:
#         return {'display': 'none'}
#
@app.callback(Output(component_id='address' , component_property='options') ,
              [Input(component_id='address' , component_property='search_value')])
def show_options(input_value):
    if not input_value:
        raise PreventUpdate
    l = input_value.split(' ')
    n = None
    for x in l:
        try:
            n = int(x)
            break
        except ValueError:
            pass
    if n is None:
        print(input_value)
        return []
    else:
        calle = ' '.join([x for x in l if x != str(n)])
        options = normalizar(calle , n)
        #print(options)
        return option_list(options)


if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0')
