#
# Handle learner profile requests
#

from pyramid.response import Response
import util, json, riak
import hashlib, base64
from webob import etag

client = riak.RiakClient(pb_port=8087, protocol='pbc')
db = client.bucket('profiles')


def getProfile(request):
	'''If authorized, respond with learner profile from db'''

	key = db.get(request.matchdict['user'])
	res = Response()

	if key.exists:

		hash = util.genETag(key.data)
		if_none_match = request.headers['If-None-Match'] if 'If-None-Match' in request.headers.keys() else None

		if if_none_match in ['*', hash]:
			res.status = 304
		else:
			res.status = 200
			res.headers['ETag'] = hash
			if request.method == 'GET':
				res.json = key.data

	else:
		res.status = 404

	return res


def saveProfile(request):
	'''If authorized, update learner profile with request body'''

	key = db.get(request.matchdict['user'])
	added = not key.exists
	data = None

	# get the post data, if available
	try:
		data = request.json
	except ValueError:
		return Response(status=400, body='Body is not JSON')	

	# compute original hash for update comparison
	if key.exists:
		oldHash = util.genETag(key.data)
	else:
		# hash of empty string
		oldHash = '1B2M2Y8AsgTpgAmY7PhCfg'

	if_match = request.headers['If-Match'] if 'If-Match' in request.headers.keys() else '*'
	if_none_match = request.headers['If-None-Match'] if 'If-None-Match' in request.headers.keys() else None

	# if the preconditions pass
	if if_match in ['*', oldHash] and if_none_match not in ['*', oldHash]:

		# merge objects on POST
		if request.method == 'POST':
			try:
				key.data = util.mergeObjects(key.data, data)
			except:
				return Response(status=500, body='Failed to merge objects')

		# replace object on PUT
		else:
			key.data = data

		key.store()

		# indicate creation or update
		res = Response(json=key.data)
		res.headers['ETag'] = util.genETag(key.data)
		res.status = 201 if added else 200
		return res

	# if the precondition fails, return 412
	else:
		return Response(status=412)


def deleteProfile(request):
	'''If authorized, delete given learner profile'''

	key = db.get(request.matchdict['user'])

	# compute original hash for update comparison
	if key.exists:
		oldHash = util.genETag(key.data)
	else:
		# hash of empty string
		oldHash = '1B2M2Y8AsgTpgAmY7PhCfg'

	if_match = request.headers['If-Match'] if 'If-Match' in request.headers.keys() else '*'
	if_none_match = request.headers['If-None-Match'] if 'If-None-Match' in request.headers.keys() else None

	# check preconditions
	if if_match in ['*',oldHash] and if_none_match not in ['*',oldHash]:
		if key.exists:
			key.delete()
			return Response(status=204)
		else:
			return Response(status=404)

	# precondition failed
	else:
		return Response(status=412)
