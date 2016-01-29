import json

def serialize(obj):

	obj_dict=obj.to_dict()
	return json.dumps(obj_dict)






