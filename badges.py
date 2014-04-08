'''
badges.py - process badge viewing and modification
'''

from pyramid.response import Response
import util, riak

client = riak.RiakClient(pb_port=8087, protocol='pbc')
db = client.bucket('profiles')


def getBadges(req):
	'''Retrieve a user's badge information'''

	key = db.get(req.matchdict['user'])
	res = Response(status=404)
	if key.exists:

		# generate proper response body
		body = None
		if 'type' not in req.matchdict:
			body = {'badges': key.data['badges']}

		elif req.matchdict['type'] in ['achieved','inprogress','desired']:
			badgeType = 'inProgress' if req.matchdict['type'] == 'inprogress' else req.matchdict['type']
			body = {badgeType: key.data['badges'][badgeType]}

		if body != None:
			hash = util.genETag(body)
			if_none_match = req.headers['If-None-Match'] if 'If-None-Match' in req.headers.keys() else None
			if if_none_match not in ['*',hash]:
				res.status = 200
				res.content_type = 'application/json'
				res.headers['ETag'] = hash
				res.json = body
			else:
				res.status = 304

	return res


def addBadges(req):
	'''Modify a list of badges'''

	key = db.get(req.matchdict['user'])

	# only take the given lists
	if req.matchdict['type'] not in ['achieved','inprogress','desired']:
		return Response(status=404)

	badgeType = 'inProgress' if req.matchdict['type'] == 'inprogress' else req.matchdict['type']

	# retrieve data
	data = None
	try:
		data = req.json
		if not isinstance(data, list):
			raise IndexError
	except ValueError:
		return Response(status=400, body='Body is not JSON')
	except IndexError:
		return Response(status=400, body='Body must be an array')

	oldHash = util.genETag({badgeType: key.data['badges'][badgeType]})
	if_match = req.headers['If-Match'] if 'If-Match' in req.headers.keys() else '*'
	if_none_match = req.headers['If-None-Match'] if 'If-None-Match' in req.headers.keys() else None

	# if the preconditions pass
	if if_match in ['*', oldHash] and if_none_match not in ['*', oldHash]:
		if req.method == 'PUT':
			key.data['badges'][badgeType] = key.data['badges'][badgeType] + data
		else:
			key.data['badges'][badgeType] = data

		key.store()

		res = Response(status=200)
		res.json = {badgeType: key.data['badges'][badgeType]}
		res.headers['ETag'] = util.genETag(res.json)
		res.content_type = 'application/json'

	else:
		res.status = 412

	return res


