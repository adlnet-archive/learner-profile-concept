'''
Miscellaneous functions
'''

import hashlib, base64, json

def mergeObjects(old, new, protectUid=False, mergeDepth=0):
	'''Update old object with data from new object'''

	# new and old are mergable
	try:
		for key in new.keys():
			try:
				# key is already in old, update
				critPath = protectUid and mergeDepth < 2 and key == ['identity','uid'][mergeDepth]
				mergedval = mergeObjects(old[key], new[key], protectUid=critPath, mergeDepth=mergeDepth+1)

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

		# protect identity.uid
		if protectUid and mergeDepth == 3:
			return old
		else:
			return new


def genETag(obj):

	md5 = hashlib.md5( json.dumps(obj,sort_keys=True) ).digest()
	return base64.b64encode(md5).strip('=')
