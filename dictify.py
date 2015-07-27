import datetime
import re

def dictify( data, includeInstanceMethods = False):
	"""
		Serializes a given python object and returns an object that is safe to be converted to a JSON string
		Serializes the given data to a json serializable format.
		1. ignores methods and instance methods
		2. Serializes instance objects to a dictionary
		3. Serializes recursivley on objects and iterable data structures
	"""
	#if function then returning nothing try to get some message
	#if str(type(data)) in ["<type 'instancemethod'>", "<type 'type'>"]:
	#	return 'function'
	#if class instance apply dictify on data.__dict__
	cls = re.compile("<class .*>").match(str(type(data)))
	if cls:
		result =  dictify(data.__dict__, includeInstanceMethods)
		if includeInstanceMethods:
			for attr in dir(data):
				if not attr.startswith('__') and not attr.endswith('__') and attr not in result:
					result[attr]= 'Instance Method'
		return result
	if type(data) in [datetime.datetime, datetime.date, datetime.time]:
		return str(data)
	dataType = re.compile("<type .*>").match(str(type(data)))
	if dataType:
		if not '__iter__' in dir(data):
			return data
	
	if type(data) in [list, set, tuple]:
		result = []
		for item in data:
			result.append(dictify(item, includeInstanceMethods))
		return result
	if type(data) == dict:
		result = {}
		for key in data.keys():
			result[key]=dictify(data[key], includeInstanceMethods)
		return result
		
