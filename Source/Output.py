from pymongo import MongoClient
import json


def serialize(employee_list):

	result=str()
	for employee in employee_list:
		emp_dict=employee.to_dict()
		result=result+json.dumps(emp_dict)
	return result


def save_to_db(db_setting,employee_list):
	client=MongoClient(db_setting["client"])
	db=client[db_setting["db"]]
	for employee in employee_list:
		emp_doc=employee.to_dict()
		db.employee.insert_one(emp_doc)



