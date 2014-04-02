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
	res = Response()
	if key.exists:

		res.status = 200
		res.content_type = 'application/json'

		if 'type' not in req.matchdict:
			res.headers['ETag'] = util.genETag(key.data['badges'])
			if req.method == 'GET':
				res.json = key.data['badges']

		elif req.matchdict['type'] == 'achieved':
			res.headers['ETag'] = util.genETag(key.data['badges']['achieved'])
			if req.method == 'GET':
				res.json = key.data['badges']['achieved']

		elif req.matchdict['type'] == 'inprogress':
			res.headers['ETag'] = util.genETag(key.data['badges']['inProgress'])
			if req.method == 'GET':
				res.json = key.data['badges']['inProgress']

		elif req.matchdict['type'] == 'desired':
			res.headers['ETag'] = util.genETag(key.data['badges']['desired'])
			if req.method == 'GET':
				res.json = key.data['badges']['desired']

		else:
			res.status = 404
			res.content_type = 'text/html'

	else:
		res.status = 404

	return res

