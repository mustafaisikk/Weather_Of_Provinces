from bs4 import BeautifulSoup
import requests
import json
from openpyxl import Workbook
import mysql.connector


class province:
    def __init__(self, code, province_name):
        self.code = code
        self.province_name = province_name


class record:
    def __init__(self, id, name, temperature, text, humidity, feels_like, time):
        self.id = id
        self.name = name
        self.temperature = temperature
        self.text = text
        self.humidity = humidity
        self.feels_like = feels_like
        self.time = time


def get_all_province_witdh_internet():
    # url = "https://www.latlong.net/category/cities-228-15.html"
    # url = "https://en.wikipedia.org/wiki/Provinces_of_Turkey"

    url = "https://kb.bullseyelocations.com/support/solutions/articles/5000695300-turkey-province-codes"

    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")

    table = soup.find("table")
    table_all_records = table.find_all("tr")

    headings = []
    for i in range(1, len(table_all_records)):
        td = table_all_records[i].find_all("td")
        name = edit_province_name(td[0].text)
        code = td[1].text
        headings.append(province(code, name))

    return headings


def edit_province_name(name):
    name = name.replace("Ç", "C")
    name = name.replace("ü", "u")
    name = name.replace("ö", "o")
    name = name.replace("â", "a")
    return name


def get_weather_of_provinces(name):
    response = requests.get(
        "http://api.weatherapi.com/v1/current.json?key={'FREE private key for each user'}&q=" + str(name))
    if response.status_code == 200:
        print("SUCCESS !!: ", name, " Data Received")
    else:
        print("ERROR !!: ", name, " Data Couldn't Be Received")
    return response.text


def create_record(id, name, response):
    temperature = json.loads(response)["current"]["temp_c"]
    text = json.loads(response)["current"]["condition"]["text"]
    humidity = json.loads(response)["current"]["humidity"]
    feels_like = json.loads(response)["current"]["feelslike_c"]
    time = json.loads(response)["location"]["localtime"]
    return record(id, name, temperature, text, humidity, feels_like, time)


def create_xlsx_file(all_records):
    wb = Workbook()
    ws = wb.active
    ws.title = "Weather Of Provinces"

    ws.append([""])
    ws.append(
        ["", "Plate_Code", "Province", "Temperature", "Text", "Humidity", "Feels_Like", "Time"])
    ws.append([""])

    for _record in all_records:
        ws.append(
            ["", _record.id, _record.name, _record.temperature, _record.text, _record.humidity, _record.feels_like,
             _record.time])

    wb.save("Weather_Of_Provinces.xlsx")


def write_database(all_records):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database="weatherofprovinces"
    )
    myCursor = mydb.cursor()
    sql = "INSERT INTO records (id, name, temperature, text, humidity, feels_like, time) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    for _record in all_records:
        val = (_record.id, _record.name, _record.temperature, _record.text, _record.humidity, _record.feels_like, _record.time)
        myCursor.execute(sql,val)

    mydb.commit()

if __name__ == '__main__':
    provinces = get_all_province_witdh_internet()

    all_records = []
    for var in provinces:
        response_text = get_weather_of_provinces(var.province_name)
        print(response_text)
        all_records.append(create_record(var.code,var.province_name,response_text))

    create_xlsx_file(all_records)
    write_database(all_records)

