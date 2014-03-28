#
# Handle learner profile requests
#

from pyramid.response import Response
import json

db = {}


def saveProfile(request):
	'''If authorized, update learner profile with request body'''

	try:
		db[request.params['id']] = request.json
		return Response(status=200, json=request.json)
	except ValueError:
		return Response(status=304, body='Body is not JSON')


def getProfile(request):
	'''If authorized, respond with learner profile from db'''

	# check for presence of profile
	if request.params['id'] not in db:
		return Response(status=404)
	else:
		return Response(json=db[request.params['id']])
