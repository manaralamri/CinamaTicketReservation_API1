from moyasar.actions.create import Create
from moyasar.resource import Resource
from moyasar.actions.cancel import Cancel
from moyasar.helpers import Format



class Invoice(Resource, Cancel, Create, Format):
    pass
    import requests
response_API = requests.get('https://gmail.googleapis.com/$discovery/rest?version=v1')
print(response_API.status_code)