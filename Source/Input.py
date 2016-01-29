import json
import csv
import Models
import PolicyFactory
import yaml
from datetime import date,timedelta,datetime

def get_current_payperiod():
	  	today=date.today()
	  	endinterval=timedelta(days=today.day)
	  	PayPeriodEndDate=today-endinterval
	  	startinterval=timedelta(days=PayPeriodEndDate.day-1)
	  	PayPeriodStartDate=PayPeriodEndDate-startinterval
	  	return (str(PayPeriodStartDate),str(PayPeriodEndDate))
	
def load_config(config_filename):

	try:
		config_dict=yaml.load(open(config_filename))
		return config_dict

	except ValueError as s:
		print ("No data found in the app.config")
	# when file name is not valid
	except IOError as i:
		print ("app.config File/URL not found")


	return
	

def load_location_data(datasource_location,pay_period):
	#This function takes csv as input and return a dictionary with location code as key value and corressponding location object for given pay period

	try:

		loc_data=csv.DictReader(open(datasource_location))
		locations_dict=dict()
		for rec in loc_data:
			if (rec["pay_period_start_date"],rec["pay_period_end_date"])==pay_period:
				locations_dict[rec["loc_code"]]=Models.Location(rec["loc_code"],rec["description"],rec["productivity"],rec["doubledown"],\
							(rec["pay_period_start_date"],rec["pay_period_end_date"]))
		return locations_dict

	except StopIteration as s:
		print ("No data found in the Locations file")
	# when file name is not valid
	except IOError as i:
		print ("Locations file not found")
	except IndexError as i:
		print ("Missing values in locations data")	

	return


def load_attendance(datasource_attendance,pay_period):
	#Returns dataset with employee's attendance for a given pay period.Returned as dictionary with emplid:attendance object pair
	try:
		att_data=csv.DictReader(open(datasource_attendance))
		att_dict=dict()
		for rec in att_data:
			if (rec["pay_period_start_date"],rec["pay_period_end_date"])==pay_period:
				att_dict[rec["empl_id"]]=Models.Attendance(rec["absence_instance"],(rec["pay_period_start_date"],rec["pay_period_end_date"]))
		return att_dict

	except StopIteration as s:
		print ("No data found in the attendance file")
	# when file name is not valid
	except IOError as i:
		print ("Attendance file not found")
	except IndexError as i:
		print ("Missing values in attendance data")
	return


def load_feedback(datasource_feedback,pay_period):
	#Returns dataset with employee's feedback for a given pay period.Returned as dictionary with emplid:feedback object pair
	try:
		fb_data=json.load(open(datasource_feedback))
		fb_dict=dict()
		for rec in fb_data:
			if (rec["pay_period_start_date"],rec["pay_period_end_date"])==pay_period:
				fb_dict[rec["empl_id"]]=Models.Feedback(rec["feedback_type"],(rec["pay_period_start_date"],rec["pay_period_end_date"]))
		return fb_dict

	except ValueError as s:
		print ("No data found in the feedback")
	# when file name is not valid
	except IOError as i:
		print ("feedback File/URL not found")
	except KeyError as k:
		print ("Invalid key in feedback data ")
	return


def load_work_per_site(datasource_sitework,datasource_location,pay_period):
	#This function takes json file as input and return a dictionary with emplid as key value and corressponding list of
	#work_per_site object for that employee as values.This will make it easy to associate these objects with employee object in load_employee function

	try:
		data=json.load(open(datasource_sitework))
		employee_work_per_site=dict()
		locations=load_location_data(datasource_location,pay_period)

		for rec in data:
			if rec["loc_code"] in locations:
				if (rec["pay_period_start_date"],rec["pay_period_end_date"])==pay_period:
					if employee_work_per_site.get(rec["empl_id"],0)==0:
						employee_work_per_site[rec["empl_id"]]=list()	
					work_per_site=Models.Work_Per_Site(locations[rec["loc_code"]],(rec["pay_period_start_date"],rec["pay_period_end_date"]),rec["worked_hours"])
					employee_work_per_site[rec["empl_id"]].append(work_per_site)
		return employee_work_per_site
	except ValueError as s:
		print ("No data found in the work at site file")
	# when file name is not valid
	except IOError as i:
		print ("work per site File/URL not found")
	except KeyError as k:
		print ("Invalid key in work per site data ")
	return


def generate_employee_data(config,pay_period):

	#Returns employee's data effective for the given pay period
	try:
		datasource=config["datasource"]
		emp_data=csv.DictReader(open(datasource["employee"]))
		work_per_site=load_work_per_site(datasource["work per site"],datasource["locations"],pay_period)
		feedback=load_feedback(datasource["feedback"],pay_period)
		attendance=load_attendance(datasource["attendance"],pay_period)	

		
		employee_list=list()
		for emp in emp_data:
			if emp["effective_date"]==pay_period[1]: # employee data effective date should be equal to pay period end date
				vcp_policy=PolicyFactory.Factory().find_employee_policy(config,emp)
				if vcp_policy.policy_type!="Ineligible":
					employee=Models.Employee(emp["empl_id"],emp["empl_name"],emp["empl_type"],emp["empl_class"],emp["jobcode"],\
						emp["cost_center"],emp["business_unit"],emp["empl_status"],emp["hourly_rt"],emp["shift_diff"],vcp_policy,\
						feedback.get(emp["empl_id"],Models.Feedback("Not Applicable",pay_period)),attendance.get(emp["empl_id"],Models.Attendance(-1,pay_period)),\
						work_per_site.get(emp["empl_id"],[]),emp["effective_date"])
					employee_list.append(employee)	

		return employee_list

	except StopIteration as s:
		print ("No data found in the employee file")
	# when file name is not valid
	except IOError as i:
		print ("employee file not found")
	except IndexError as i:
		print ("Missing values in employee data")	
	except KeyError as k:
		print ("Invalid key in config dict ")
	return






