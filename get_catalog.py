###### Script para sacar la información del Cenace
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import requests
import time
import xlrd
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 
#driver = webdriver.Chrome('/home/andres/Dropbox/energy_dev/utils/chromedriver', chrome_options=chrome_options, service_args=['--verbose', '--log-path=/home/andres/Dropbox/energy_dev/utils/chromedriver.log'])

#dirver folder
#driver_folder = '/home/andres/Dropbox/energy_dev/utils/'
driver_folder = '/usr/bin/'

#cargar el webdriver
driver = webdriver.Chrome(driver_folder + 'chromedriver', chrome_options = chrome_options)

time.sleep(5)

# link como a la pagina
driver.get("https://www.cenace.gob.mx/Paginas/Publicas/MercadoOperacion/NodosP.aspx")

time.sleep(10)

element_list = driver.find_elements_by_css_selector("[href]")

# listar los elementos
element_list_values = []
for element in element_list:
	element_value = element.get_attribute("href")
	element_list_values.append(element_value)

time.sleep(5)
csvs = [v for v in element_list_values if v.endswith(".xlsx")]  

#seleccionar el catalogo mas nuevo
catalogo_nodos = csvs[0]

#bajar el catalogo en xlsx
data=requests.get(catalogo_nodos, verify=False)
workbook = xlrd.open_workbook(file_contents=data.content)
worksheet = workbook.sheet_by_index(0)

#crear el data set
offset = 0
rows = []
for i, row in enumerate(range(worksheet.nrows)):
    if i <= offset:  # (Optionally) skip headers
        continue
    r = []
    for j, col in enumerate(range(worksheet.ncols)):
        r.append(worksheet.cell_value(i, j))
    rows.append(r)

#convertir el dataset a un dataframe de pandas
df = pd.DataFrame.from_records(rows[1::], columns=rows[0])

#seleccionar el folder en donde se va a aguardar el catalogo
destination_folder = "/data/"

#guardar el catalogo mas reciente con la fecha en la que se ejecuta el script
today = datetime.today().strftime("%d-%m-%Y")
df.to_csv(destination_folder + str(datetime.today().strftime("%d-%m-%Y")) + "_catalogo_nodos.csv", index=False)

