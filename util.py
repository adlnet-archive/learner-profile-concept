'''
Miscellaneous functions
'''

def mergeObjects(old, new):
	'''Update old object with data from new object'''

	# new and old are mergable
	try:
		for key in new.keys():
			try:
				# key is already in old, update
				old[key] = mergeObjects(old[key], new[key])
			except KeyError:
				# key is not in old, create
				old[key] = new[key]

		return old if old != None else new

	# new and old are not mergable, so new is the updated value
	except (TypeError, AttributeError):
		return new
