'''
Miscellaneous functions
'''

import hashlib, base64, json

def mergeObjects(old, new):
	'''Update old object with data from new object'''

	# new and old are mergable
	try:
		for key in new.keys():
			try:
				# key is already in old, update
				mergedval = mergeObjects(old[key], new[key])
				if mergedval != None:
					old[key] = mergedval
				else:
					del old[key]

			except KeyError:
				# key is not in old, create
				old[key] = new[key]

		return old if old != None else new

	# new and old are not mergable, so new is the updated value
	except (TypeError, AttributeError):
		return new


def genETag(obj):

	md5 = hashlib.md5( json.dumps(obj,sort_keys=True) ).digest()
	return base64.b64encode(md5).strip('=')
