import requests

def requestsVersion():
    print('Requests Version:', requests.__version__)

def statusCode():
    request = requests.get("http://www.google.com/")
    print('\n Status code:', request.status_code)

def script():
    request = requests.get("http://www.google.com/")
    print('\n raw URL:',request.text)


requestsVersion()
statusCode()
script()

