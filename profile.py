'''
profile.py - Process direct learner profile requests
'''

from pyramid.response import Response
import util, riak, copy
import hashlib, base64

client = riak.RiakClient(pb_port=8087, protocol='pbc')
db = client.bucket('profiles')

profileSkeleton = {
	'identity': {
		'userid': None
	},
	'badges': {
		'desired': [],
		'inProgress': [],
		'achieved': []
	}
}

def createProfile(request):
	'''Create a new learner profile'''

	# get proposed key
	uid = None
	try:
		uid = request.json['identity']['userid']
	except ValueError:
		return Response(status=400, body='Body is not JSON')
	except KeyError:
		return Response(status=400, body='Body does not include required field "identity.userid"')

	if db.get(uid).exists:
		return Response(status=409)
	
	# create stub profile
	template = copy.deepcopy(profileSkeleton)
	data = util.mergeObjects(template, request.json, protectUid=False)
	key = db.new(uid, data=data)
	key.store()

	res = Response(status=201, json=data)
	res.headers['ETag'] = util.genETag(data)

	return res


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
				res.content_type = 'application/json'

	else:
		res.status = 404

	return res


def saveProfile(request):
	'''If authorized, update learner profile with request body'''

	key = db.get(request.matchdict['user'])
	data = None

	# get the post data, if available
	try:
		data = request.json
	except ValueError:
		return Response(status=400, body='Body is not JSON')	

	if not key.exists:
		return Response(status=404)

	# compute original hash for update comparison
	oldHash = util.genETag(key.data)
	if_match = request.headers['If-Match'] if 'If-Match' in request.headers.keys() else '*'
	if_none_match = request.headers['If-None-Match'] if 'If-None-Match' in request.headers.keys() else None

	# if the preconditions pass
	if if_match in ['*', oldHash] and if_none_match not in ['*', oldHash]:

		# merge objects on PUT
		if request.method == 'PUT':
			try:
				key.data = util.mergeObjects(key.data, data, protectUid=True)
			except:
				return Response(status=500, body='Failed to merge objects')

		# replace object on POST
		else:
			template = copy.deepcopy(profileSkeleton)
			template['identity']['userid'] = request.matchdict['user']
			key.data = util.mergeObjects(template, data, protectUid=True)

		key.store()

		# indicate creation or update
		res = Response(json=key.data)
		res.headers['ETag'] = util.genETag(key.data)
		res.status = 200
		return res

	# if the precondition fails, return 412
	else:
		return Response(status=412)


def deleteProfile(request):
	'''If authorized, delete given learner profile'''

	key = db.get(request.matchdict['user'])

	if not key.exists:
		return Response(status=404)

	# compute original hash for update comparison
	oldHash = util.genETag(key.data)
	if_match = request.headers['If-Match'] if 'If-Match' in request.headers.keys() else '*'
	if_none_match = request.headers['If-None-Match'] if 'If-None-Match' in request.headers.keys() else None

	# check preconditions
	if if_match in ['*',oldHash] and if_none_match not in ['*',oldHash]:
		key.delete()
		return Response(status=204)

	# precondition failed
	else:
		return Response(status=412)
