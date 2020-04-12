import json  # json package
import requests  # requests package

def api4():
    print '#' * 40
    print 'Welcome to API 4'
    cname = raw_input('enter city name or q to quit: ')  # input city name for which data is required
    if cname == "q":
        print "END OF API 4"
        print '#' * 40
        return
    data = requests.get('http://api.openweathermap.org/data/2.5/weather?appid=4b1c22a0a3ffed57f0dfec3154b50ad9&q=' + cname + '')  # Requesting data from the url
    data_format = json.loads(data.text)  # Extracting text from the data
    if str(data_format['cod']) == "404":  # checking if city is not found or city name is wrong
        print (data_format['message'])  # Displaying Error message
    else:
        temp_k = float(data_format['main']['temp'])  # Extracting temp value from the data
        pressure = float(data_format['main']['pressure'])  # Extracting pressure value from the data
        humidity = float(data_format['main']['humidity'])  # Extracting humidity value from the data
        temp_f = temp_k - 273.15  # converting temp degree kelvin to degree celsius
        print("temperature: " + str(round(temp_f, 2)))  # Rounding values and printing them
        print("pressure: " + str(round(pressure, 2)))
        print("humidity: " + str(round(humidity, 2)))
        print "END OF API 4"
        print '#' * 40