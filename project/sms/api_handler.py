import wikipedia
import googlemaps
import re
import forecastio
from ohmysportsfeedspy import MySportsFeeds

gmaps_key = "AIzaSyArLBOGZk0mH_VKEMUjnyvLLLNRR2w9BcA"
forecast_key = "9acf53a7de55294989b3f3904e8a8d57"
msf = MySportsFeeds(version="1.2", store_type=None, store_location=None)
msf.authenticate("kvanderheiden", "lucidata506")

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

    loc_type = data[0]   #indicates whether location is a coordinate ('c') or address('a')
    forecast_type = data[1]   #indicates whether forecast should be alert('a'), 24-hour('2'), or 7-day('7')
    loc = data[2:]   #location for which to get forecast
    forecast = ''

    if loc_type == 'c':
        loc = loc.split(';')
        lat = loc[0]
        lng = loc[1]

    #if address is provided, geocode to lat/lng coordinates
    elif loc_type == 'a':
        gmapsResponse = googlemaps.geocoding.geocode(cli, loc)
        lat = gmapsResponse[0]['geometry']['location']['lat']
        lng = gmapsResponse[0]['geometry']['location']['lng']

    response = forecastio.load_forecast(forecast_key,lat=lat,lng=lng,units="us")

    #get alerts
    if forecast_type == 'a':
        alerts = response.alerts()
        if len(alerts) != 0:
            for alert in alerts:
                forecast = forecast + alert.title + '//'
            forecast = forecast[:-2]
        else:
            forecast = "No weather alerts"

    #get 24-hour forecast
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

    #get 7-day forecast
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

def sports_handler(data):
    '''
    Calls to MySportsFeeds API are made here to gather information about games.
    Data should be a string that includes the league ('b' for NBA, 'f' for NFL,
    'h' for NHL, or 'm' for MLB), followed by the date (formatted as yyyymmdd).
    Returns a string with information about each game in the specified league
    on the given date. Each game is separated by '/'. Each piece of game information
    is separated by ';'. The first two elements for each game are the name of the away
    team and the name of the home team. The next element is the status (a time if the game
    has not been played yet, 'p' if the game is in progress, or 'f' if the game is finished).
    If the game is finished, there will be two more elements: the away team's score and
    the home team's score.
    '''
    start_time = ''
    away_score = ''
    home_score = ''
    away_team = ''
    home_team = ''
    response = ''

    league = data[0]
    if(data[0] == 'b'):
        league = 'nba'
    elif(data[0] == 'f'):
        league = 'nfl'
    elif(data[0] == 'h'):
        league = 'nhl'
    elif(data[0] == 'm'):
        league = 'mlb'
    date = data[1:9]    #date formatted as yyyymmdd

    try:
        stats = msf.msf_get_data(league=league, season='current', feed='scoreboard', format='json', fordate=date, force='true')
        game_stats = stats['scoreboard']['gameScore']
    except:
        return ('No ' + league + ' games found on ' + date[4:6] + '/' + date[6:8] + '/' + date[0:4])

    for game in game_stats:
        away_team = game['game']['awayTeam']['Name']
        home_team = game['game']['homeTeam']['Name']
        if game['isUnplayed'] == 'true':
            start_time = game['game']['time']
        elif game['isInProgress'] == 'true':
            start_time = 'p'
        elif game['isCompleted'] == 'true':
            start_time = 'f'
            away_score = game['awayScore']
            home_score = game['homeScore']
        response = response + away_team + ';'
        response = response + home_team + ';'
        response = response + start_time + ';'
        if(away_score != '' and home_score != ''):
            response = response + away_score + ';'
            response = response + home_score + ';'
        response = response[:-1] + '/'
    response = response[:-1]

    return response
