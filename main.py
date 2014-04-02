from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

import sys
import profile, badges



def main(args):

	config = Configurator()

	# configure full profile editing
	config.add_route('getProfile', pattern='/learner/{user}', request_method=('GET','HEAD'))
	config.add_view(profile.getProfile, route_name='getProfile')
	config.add_route('saveProfile', pattern='/learner/{user}', request_method=('POST','PUT'))
	config.add_view(profile.saveProfile, route_name='saveProfile')
	config.add_route('deleteProfile', pattern='/learner/{user}', request_method='DELETE')
	config.add_view(profile.deleteProfile, route_name='deleteProfile')

	# configure badge views
	config.add_route('getBadges', pattern='/learner/{user}/badges', request_method=('GET','HEAD'))
	config.add_route('getBadgeType', pattern='/learner/{user}/badges/{type}', request_method=('GET','HEAD'))
	config.add_view(badges.getBadges, route_name='getBadges')
	config.add_view(badges.getBadges, route_name='getBadgeType')

	config.add_static_view('static', 'static/')

	app = config.make_wsgi_app()
	server = make_server('0.0.0.0', 8080, app)

	# launch server
	print 'Server active on {0[0]}:{0[1]}'.format(server.server_address)
	print 'Ctrl-c to quit...'
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print 'Exiting'
		quit()


if __name__ == '__main__':
	main(sys.argv)
