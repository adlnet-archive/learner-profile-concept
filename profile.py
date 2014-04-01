#
# Handle learner profile requests
#

from pyramid.response import Response
import util, json, riak

client = riak.RiakClient(pb_port=8087, protocol='pbc')
db = client.bucket('profiles')


def getProfile(request):
	'''If authorized, respond with learner profile from db'''

	key = db.get(request.params['id'])
	res = Response()

	if key.exists:

		res.status = 200
		res.md5_etag( json.dumps(key.data, sort_keys=True) )
		if request.method == 'GET':
			res.json = key.data

	else:
		res.status = 404

	return res


def saveProfile(request):
	'''If authorized, update learner profile with request body'''

	key = db.get(request.params['id'])
	data = None
	try:
		data = request.json
	except ValueError:
		return Response(status=304, body='Body is not JSON')	


	if request.method == 'POST':
		try:
			key.data = util.mergeObjects(key.data, data)
		except:
			return Response(status=500, body='Failed to merge objects')
	else:
		key.data = data

	key.store()
	return Response(status=200, json=key.data)


def deleteProfile(request):
	'''If authorized, delete given learner profile'''

	key = db.get(request.params['id'])
	if key.exists:
		key.delete()
		return Response(status=200)
	else:
		return Response(status=404)
