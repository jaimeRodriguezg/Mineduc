from bs4 import BeautifulSoup
import requests

headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
}

def get_info_colegio(codigo, nombre_colegio):
  print(nombre_colegio)
  data = {"nombre": nombre_colegio}
  params = {
    "rbd": codigo
  }
  response = requests.post("https://www.mime.mineduc.cl/mime-web/mvc/mime/ficha", headers = headers, params = params)

  page = BeautifulSoup(response.content, "lxml")
  info = page.find("table", class_ = "tabla_form").find_all("tr", recursive=False)
  campos = ["direccion","", "comuna", "telefono", "email", "webpage", "director", "sostenedor"]
  for i,dato in enumerate(info):
    if i != 1:
      welp = dato.find_all("td")
      data[campos[i]] = welp[1].text.strip()
  
  dep = page.find("div", id = "ver1").find_all("div", recursive=False)[2].find("div", class_ = "form_detalle").text
  data["dependencia"] = dep
  return data


regiones = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

comunas = [['1101','1107','1401','1402','1403','1404','1405'],['2101','2102','2103','2104','2201','2202','2203','2301','2302'],['3101','3102','3103','3201','3202','3301','3302','3303','3304'],['4101','4102','4103','4104','4105','4106','4201','4202','4203','4204','4301','4302','4303','4304','4305'],['5101','5102','5103','5104','5105','5107','5109','5201','5301','5302','5303','5304','5401','5402','5403','5404','5405','5501','5502','5503','5504','5506','5601','5602','5603','5604','5605','5606','5701','5702','5703','5704','5705','5706','5801','5802','5803','5804'],['6101','6102','6103','6104','6105','6106','6107','6108','6109','6110','6111','6112','6113','6114','6115','6116','6117','6201','6202','6203','6204','6205','6206','6301','6302','6303','6304','6305','6306','6307','6308','6309','6310'],['7101','7102','7103','7104','7105','7106','7107','7108','7109','7110','7201','7202','7203','7301','7302','7303','7304','7305','7306','7307','7308','7309','7401','7402','7403','7404','7405','7406','7407','7408'],['8101','8102','8103','8104','8105','8106','8107','8108','8109','8110','8111','8112','8201','8202','8203','8204','8205','8206','8207','8301','8302','8303','8304','8305','8306','8307','8308','8309','8310','8311','8312','8313','8314'],['9101','9102','9103','9104','9105','9106','9107','9108','9109','9110','9111','9112','9113','9114','9115','9116','9117','9118','9119','9120','9121','9201','9202','9203','9204','9205','9206','9207','9208','9209','9210','9211'],['10101','10102','10103','10104','10105','10106','10107','10108','10109','10201','10202','10203','10204','10205','10206','10207','10208','10209','10210','10301','10302','10303','10304','10305','10306','10307','10401','10402','10403','10404'],['11101','11102','11201','11202','11203','11301','11302','11303','11401','11402'],['12101','12102','12103','12104','12201','12202','12301','12302','12303','12401','12402'],['13101','13102','13103','13104','13105','13106','13107','13108','13109','13110','13111','13112','13113','13114','13115','13116','13117','13118','13119','13120','13121','13122','13123','13124','13125','13126','13127','13128','13129','13130','13131','13132','13201','13202','13203','13301','13302','13303','13401','13402','13403','13404','13501','13502','13503','13504','13505','13601','13602','13603','13604','13605'],['14101','14102','14103','14104','14105','14106','14107','14108','14201','14202','14203','14204'],['15101','15102','15201','15202'],['16101','16102','16301','16302','16201','16103','16104','16303','16202','16105','16106','16304','16107','16305','16306','16203','16204','16108','16205','16307','16109']]


def get_colegios_region(region):
  data = []
  params = {
    "reg": region,
    "com": "",
    "dep": 0,
    "npar": 0,
    "nbas": 0,
    "nmed": 0,
    "sep": 0,
    "tens": 0,
    "esp": 0,
    "sec": 0,
    "espec": 0,
    "rbd1": "",
    "region": region,
    "comuna": "",
    "dependencia": 0,
    "idMedia": 1,
    "tipoEns": 0,
    "sectorEco": 0,
    "especialidad": 0,
    "nEspecial": 0
  }

  for comuna in comunas[region-1]:
    params["com"] = params["comuna"] = comuna
    print(comuna)
    response = requests.post("https://www.mime.mineduc.cl/mime-web/mvc/mime/busqueda_avanzada", headers = headers, params = params)

    page = BeautifulSoup(response.content, "lxml")

    try:
      colegios = page.find("table", id ="busqueda_avanzada").find("tbody").find_all("td", recursive = True)
    except Exception as e:
      print("NO HAY TABLA CON COLEGIOS ",repr(e))
      continue

    for colegio in colegios:
      try:
        is_colegio = colegio.find("a")
        if is_colegio:
          codigo = colegio.text.split("[")[-1].strip().split("]")[0]
          info = get_info_colegio(codigo, colegio.text.split("[")[0].strip())
          data.append(info)
      except Exception as e:
        print("COLEGIO MURIÓ", repr(e))

  return data

info = get_colegios_region(16)
with open("DeÑuble.csv", "w") as file:
  file.write("Nombre,Direccion,Comuna,Telefono,Email,Webpage,Director,Sostenedor,Dependencia\n")
  for colegio in info:
    nombre = colegio["nombre"]
    direccion = colegio["direccion"]
    comuna = colegio["comuna"]
    telefono = colegio["telefono"]
    email = colegio["email"]
    webpage = colegio["webpage"]
    director = colegio["director"]
    sostenedor = colegio["sostenedor"]
    dependencia = colegio["dependencia"]
    file.write(f"{nombre},{direccion},{comuna},{telefono},{email},{webpage},{director},{sostenedor},{dependencia}\n")