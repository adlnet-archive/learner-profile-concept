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
				res.json = {'badges': key.data['badges']}

		elif req.matchdict['type'] == 'achieved':
			body = {'achieved': key.data['badges']['achieved']}
			res.headers['ETag'] = util.genETag(body)
			if req.method == 'GET':
				res.json = body

		elif req.matchdict['type'] == 'inprogress':
			body = {'inProgress': key.data['badges']['inProgress']}
			res.headers['ETag'] = util.genETag(body)
			if req.method == 'GET':
				res.json = body

		elif req.matchdict['type'] == 'desired':
			body = {'desired': key.data['badges']['desired']}
			res.headers['ETag'] = util.genETag(body)
			if req.method == 'GET':
				res.json = body

		else:
			res.status = 404
			res.content_type = 'text/html'

	else:
		res.status = 404

	return res

