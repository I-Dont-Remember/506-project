import wikipedia

MAX_CHAR = 156

def api_handler(app, data):
    '''
    This acts as an interface between the sms handler and call
    to an external API.
    Data is retreived from a specific API and sent back to the sms handler
    '''
    # determine API to call based on app param
    if app.name == "wikipedia":
        return wiki_handler(data)
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
