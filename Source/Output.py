import json

def serialize(obj):
	try:	
		for attr, value in obj.__dict__.items():
			print(json.dumps(value))

	except TypeError as t:
		serialize(value)







