import wikipedia
import googlemaps
import re
import forecastio

gmaps_key = "AIzaSyArLBOGZk0mH_VKEMUjnyvLLLNRR2w9BcA"
forecast_key = "9acf53a7de55294989b3f3904e8a8d57"

MAX_CHAR = 156

cli = googlemaps.Client(key=gmaps_key)

def api_handler(app, data):
    '''
    This acts as an interface between the sms handler and call
    to an external API.
    Data is retreived from a specific API and sent back to the sms handler
    '''
    # determine API to call based on app param
    if app.name == "wikipedia":
        return wiki_handler(data)
    if app.name == "directions":
        return dir_handler(data)
    if app.name == "weather":
        return weather_handler(data)
    if app.name == "sports":
        return sports_handler(data)
    return None

def wiki_handler(data):
    '''
    Wikipedia API calls are made here, with the subject as data.
    Returns a summary limited to 154 characters from the closest
    matching entry.
    '''
    # retreive data
    try:
        response = wikipedia.summary(data)
    except wikipedia.exceptions.PageError:
        response = "No Wikipedia entry found for " + data

    # cut off data at max text length
    if len(response) > MAX_CHAR:
        response = response[0:153] + "..."

    return response

def dir_handler(data):
    '''
    Calls to the Google Maps API are made here. Data should contain
    a start location and a destination separated by a semicolon.
    Locations can be addresses or lat/lng coordinates. Returns a string
    of directions separated by semicolons.
    '''

    dir = ''
    data = data.split(';')
    start_loc = data[0]
    dest_loc = data[1]
    
    try:
        dir_response = googlemaps.directions.directions(cli, origin=start_loc, destination=dest_loc)
    except googlemaps.exceptions.ApiError:
        return "Directions not found for " + start_loc + " to " + dest_loc
    
    steps = dir_response[0]['legs'][0]['steps']

    for step in steps:
        formatted = re.sub('<div.*?>', '. ', step['html_instructions'])
        formatted = re.sub('<.*?>', '', formatted)
        dir = dir + '(' + step['distance']['text'] + ') ' + formatted + ';'
    dir = dir[:-1]

    return dir

def weather_handler(data):
    '''
    Calls to the Dark Sky API are made here to gather weather forecasts.
    Data should be a string that includes the location type ('c' for lat/lng; 'a' for an address),
    followed by the forecast type ('a' for alerts; '2' for 24-hour; '7' for 7-day), followed by
    the location (formatted as lat;lng or an address). Returns a string of weather data. For alerts,
    if there are mulitple alerts they are separated by '//'. Each alert is just a single description.
    For 24-hour, hours are separated by '/'. Each hour has a desciprtion, followed by the temperature, 
    followed optionally by a precipitation type and precipitation probability (each separated by ';'). 
    For 7-day, days are separated by '/'. Each day has a description, followed by the high temp, 
    followed by the low temp, followed optionally by a precipitation type and precipitation probability 
    (each separated by ';').
    '''

    loc_type = data[0]
    forecast_type = data[1]
    loc = data[2:]
    forecast = ''
    
    if loc_type == 'c':
        loc = loc.split(';')
        lat = loc[0]
        lng = loc[1]
    elif loc_type == 'a':
        gmapsResponse = googlemaps.geocoding.geocode(cli, loc)
        lat = gmapsResponse[0]['geometry']['location']['lat']
        lng = gmapsResponse[0]['geometry']['location']['lng']

    response = forecastio.load_forecast(forecast_key, lat=lat, lng=lng,units="us")

    if forecast_type == 'a':
        alerts = response.alerts()
        if len(alerts) != 0:
            for alert in alerts:
                forecast = forecast + alert.title + '//'
            forecast = forecast[:-2]
        else:
            forecast = "No weather alerts"
        
    elif forecast_type == '2':
        hourly = response.hourly().data
        for hour in hourly:
            forecast = forecast + hour.icon + ';'
            forecast = forecast + str(round(hour.temperature)) + ';'
            try:
                forecast = forecast + hour.precipType + ';'
                forecast = forecast + "{:.2f}".format(hour.precipProbability)
            except forecastio.utils.PropertyUnavailable:
                forecast = forecast[:-1]
            forecast = forecast + '/'

    elif forecast_type == '7':
        daily = response.daily().data
        for day in daily:
            forecast = forecast + day.icon + ';'
            forecast = forecast + str(round(day.temperatureHigh)) + ';'
            forecast = forecast + str(round(day.temperatureLow)) + ';'
            try:
                forecast = forecast + day.precipType + ';'
                forecast = forecast + "{:.2f}".format(day.precipProbability)
            except forecastio.utils.PropertyUnavailable:
                forecast = forecast[:-1]
            forecast = forecast + '/'

    return forecast

#def sports_handler(data):
