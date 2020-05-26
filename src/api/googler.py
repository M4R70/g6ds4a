import requests
import json
resp = requests.get("https://ws.usig.buenosaires.gob.ar/rest/normalizar_y_geocodificar_direcciones", params={"calle":"scalabrini ortiz","altura":"200","desambiguar":1})
#print(resp.text)

d = json.loads(resp.text)

for x,y in d.items():
    print(f"{x}  {y}")
