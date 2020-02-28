import logging
import os
import connexion
from time import time
from libs.utils import Utils


countries_list = Utils.external_request(os.environ.get('REGIONS_URL'))
regions = []
countries = []
languages = []
times = []
for country in countries_list:
    # se agrega condicion de si es vacio porque me devuelve una region vacia en alguno de los paises
    if not country['region'] in regions and country['region'] != '':
        time_start = time()  # iniciando conteo de generación de la fila
        regions.append(country['region'])
        resp = Utils.external_request('{}/{}'.format(os.environ.get('COUNTRY_URL'), country['region']))
        countries.append(resp[0]['name'])
        languages.append(Utils.encrypt(resp[0]['languages'][0]['name']))
        times.append(round(time() - time_start, 2))

data = {
    'region': regions,
    'country': countries,
    'language': languages,
    'time': times
}

Utils.data_frame(data)

sh = logging.StreamHandler()
logging.basicConfig(format='%(asctime)s |%(name)s|%(levelname)s|%(message)s',
                    level=logging.INFO,
                    handlers=[sh])

connx_app = connexion.App(__name__, specification_dir='./')
connx_app.add_api('swagger.yaml')
app = connx_app.app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
