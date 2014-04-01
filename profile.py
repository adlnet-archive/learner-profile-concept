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

	key = db.get(request.params['id'])
	res = Response()

	if key.exists:

		res.md5_etag( json.dumps(key.data, sort_keys=True) )

		if request.if_none_match == res.etag:
			res.status = 304
		else:
			res.status = 200
			if request.method == 'GET':
				res.json = key.data

	else:
		res.status = 404

	return res


def saveProfile(request):
	'''If authorized, update learner profile with request body'''

	key = db.get(request.params['id'])
	added = not key.exists
	data = None

	# get the post data, if available
	try:
		data = request.json
	except ValueError:
		return Response(status=400, body='Body is not JSON')	

	# compute original hash for update comparison
	if key.exists:
		oldHash = hashlib.md5( json.dumps(key.data, sort_keys=True) ).digest()
		oldHash = base64.b64encode(oldHash).strip('=')
	else:
		oldHash = None

	#print 'If "{!r}", If not "{!r}"'.format(request.if_match, request.if_none_match)
	#print type(request.if_match)
	#matcher = etag.ETagMatcher([oldHash])

	# if the preconditions pass
	if request.if_match in [etag.AnyETag, oldHash] and request.if_none_match not in [etag.NoETag, oldHash]:

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
		if added:
			return Response(status=201, json=key.data)
		else:
			return Response(status=200, json=key.data)

	# if the precondition fails, return 412
	else:
		return Response(status=412)


def deleteProfile(request):
	'''If authorized, delete given learner profile'''

	key = db.get(request.params['id'])
	if key.exists:
		key.delete()
		return Response(status=204)
	else:
		return Response(status=404)
