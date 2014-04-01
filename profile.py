#
# Handle learner profile requests
#

from pyramid.response import Response
import json
import riak

client = riak.RiakClient(pb_port=8087, protocol='pbc')
db = client.bucket('profiles')


def saveProfile(request):
	'''If authorized, update learner profile with request body'''

	key = db.get(request.params['id'])
	try:
		key.data = request.json
		key.store()
		return Response(status=200, json=key.data)

	except ValueError:
		return Response(status=304, body='Body is not JSON')	
	except e:
		return Response(status=500, body=e)

def getProfile(request):
	'''If authorized, respond with learner profile from db'''

	key = db.get(request.params['id'])
	if key.data == None:
		return Response(status=404)
	else:
		return Response(status=200, json=key.data)
