from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

import sys
import profile



def main(args):

	config = Configurator()

	config.add_route('getProfile', '/profile', request_method=('GET','HEAD'), request_param='id')
	config.add_route('saveProfile', '/profile', request_method=('POST','PUT'), request_param='id')
	config.add_route('deleteProfile', '/profile', request_method='DELETE', request_param='id')

	config.add_view(profile.getProfile, route_name='getProfile')
	config.add_view(profile.saveProfile, route_name='saveProfile')
	config.add_view(profile.saveProfile, route_name='deleteProfile')

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
