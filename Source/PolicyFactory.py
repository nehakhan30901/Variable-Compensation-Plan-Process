class Ineligible_for_VCP:

	def __init__(self):
		self.policy_type="Ineligible"

#Defining US FC policy
class US_FC_VCP_Policy:

	def __init__(self,config_dict):
		self.policy_type="US FC VCP Policy"
		self.attendance_payout=config_dict["attendance_payout"]["US FC"]
		self.paycode_rate=config_dict["paycode_rate"]["US FC"]

	def calc_eligible_earnings(self,worked_hours):
 		eligible_earnings=0
 		for paycode in self.paycode_rate:
 			eligible_earnings=eligible_earnings+(float(self.paycode_rate[paycode])*float(worked_hours[paycode]))
 		return eligible_earnings

	def calc_vcp_percent(self,attendance,feedback,location):

			vcp_percent=float(self.attendance_payout.get(attendance.absence_instance,0))+float(location.productivity)
			return vcp_percent


#Defining US CS policy
class US_CS_VCP_Policy:

	def __init__(self,config_dict):
		self.policy_type="US CS VCP Policy"
		self.attendance_payout=config_dict["attendance_payout"]["US CS"]
		self.feedback_payout=config_dict["feedback_payout"]["US CS"]
		self.paycode_rate=config_dict["paycode_rate"]["US CS"]

	def calc_eligible_earnings(self,worked_hours):
 		eligible_earnings=0
 		for paycode in self.paycode_rate:
 			eligible_earnings=eligible_earnings+(float(self.paycode_rate[paycode])*float(worked_hours[paycode]))
 		return eligible_earnings

	def calc_vcp_percent(self,attendance,feedback,location):

			vcp_percent=(float(self.attendance_payout.get(attendance.absence_instance,0))\
					+self.feedback_payout.get(feedback.feedback_type,0)+float(location.productivity)+float(location.doubledown))
			return vcp_percent


#FACTORY FUNCTION comprising object creation logic based on policy

class Factory:

	def __init__(self):
		pass

	def get_eligible_policy(self,policy,config_dict):	

		if policy=="US FC":
			return US_FC_VCP_Policy(config_dict)
		elif policy=="US CS":
			return US_CS_VCP_Policy(config_dict)
		else:
			return Ineligible_for_VCP()

	def find_employee_policy(self,config,employee):

		eligible_policy="Ineligible"

		for policy in config["eligibility_criteria"]:
			if  employee["empl_type"] not in config["eligibility_criteria"][policy].get("empl_type",[]):
				 continue
			elif employee["empl_class"] not in config["eligibility_criteria"][policy].get("empl_class",[]):
				continue

			elif employee["business_unit"]not in config["eligibility_criteria"][policy].get("business_unit",[]):
				continue
			elif employee["jobcode"] not in config["eligibility_criteria"][policy].get("jobcode",[]):
				continue
			elif employee["cost_center"] not in config["eligibility_criteria"][policy].get("cost_center",[]):
				continue
			else:
				#allocating the eligible policy to employee
				eligible_policy=policy

		return self.get_eligible_policy(eligible_policy,config)

	



