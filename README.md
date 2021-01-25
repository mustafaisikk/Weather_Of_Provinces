Bu projede öncelikle web scraping ile Türkiye'nin bütün illerini ve plaka kodlarını elde ettim. Ardından bir api sağlayıcısından bu iller ile ilgili o anlık hava durumu bilgilerini çektim. Daha sonra bu bilgileri hem Excel dosyasına hem de MySQL veri tabanına yazdım. 
Bu projemde kullandığım kaynaklar:
- Web Scraping (Veri Kazıma)
	- https://kb.bullseyelocations.com/support/solutions/articles/5000695300-turkey-province-codes

	-	```python
		def get_all_province_witdh_internet():  
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
		```
- Api Sağlayıcısı
	- http://api.weatherapi.com/
	- ```python
		def get_weather_of_provinces(name):  
		    response = requests.get(  
		        "http://api.weatherapi.com/v1/current.json?key={'FREE private key for each user'}&q=" + str(name))  
		    if response.status_code == 200:  
		        print("SUCCESS !!: ", name, " Data Received")  
		    else:  
		        print("ERROR !!: ", name, " Data Couldn't Be Received")  
		    return response.text
		```
		
