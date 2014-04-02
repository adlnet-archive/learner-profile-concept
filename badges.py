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
		if 'type' not in req.matchdict:
			res.json = key.data['badges']
		elif req.matchdict['type'] == 'achieved':
			res.json = key.data['badges']['achieved']
		elif req.matchdict['type'] == 'inprogress':
			res.json = key.data['badges']['inProgress']
		elif req.matchdict['type'] == 'desired':
			res.json = key.data['badges']['desired']
		else:
			res.status = 404

	else:
		res.status = 404

	return res

