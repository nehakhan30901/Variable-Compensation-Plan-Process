#This module defines all the entities used by the VCP Project
import PolicyFactory
import json
import Input

#DEFINING Employee entity

class Employee:

	def __init__(self,empl_id,empl_name,empl_type,empl_class,jobcode,cost_center,business_unit,empl_status,hourly_rt,shift_diff,\
				 vcp_policy,feedback,attendance,work_per_site,effective_date):
		self.empl_id=empl_id
		self.empl_name=empl_name
		self.empl_type=empl_type
		self.empl_class=empl_class
		self.jobcode=jobcode
		self.cost_center=cost_center
		self.business_unit=business_unit
		self.empl_status=empl_status
		self.hourly_rt=hourly_rt
		self.shift_diff=shift_diff
		self.feedback=feedback
		self.attendance=attendance
		self.work_per_site=work_per_site
		self.effective_date=effective_date
		self.payrate=float(self.hourly_rt)+float(self.shift_diff)
		self.vcp_policy=vcp_policy
		self.vcp_payout=0
		#self.site_effort
		

	def process_employee_vcp(self):

		for site in self.work_per_site:	

				#Get VCP components
			site.eligible_earnings=self.vcp_policy.calc_eligible_earnings(site.worked_hours)
			site.vcp_percent=self.vcp_policy.calc_vcp_percent(self.attendance,self.feedback,site.location)	

				#Calculate vcp amount per site
			site.vcp_payout=float(site.eligible_earnings)*float(site.vcp_percent)*float(self.payrate)	

				#Sum up for total amount
			self.vcp_payout=self.vcp_payout+site.vcp_payout


	def to_dict(self):
		"serialize object"

		obj_as_dict=dict()

		obj_as_dict["empl_id"]=self.empl_id
		obj_as_dict["empl_name"]=self.empl_name
		obj_as_dict["empl_type"]=self.empl_type
		obj_as_dict["empl_class"]=self.empl_class
		obj_as_dict["jobcode"]=self.jobcode
		obj_as_dict["cost_center"]=self.cost_center
		obj_as_dict["business_unit"]=self.business_unit
		obj_as_dict["empl_status"]=self.empl_status
		obj_as_dict["hourly_rt"]=self.hourly_rt
		obj_as_dict["shift_diff"]=self.shift_diff
		obj_as_dict["vcp_policy"]=self.vcp_policy.policy_type
		obj_as_dict["feedback"]=self.feedback.feedback_type
		obj_as_dict["attendance_instances"]=self.attendance.absence_instance
		obj_as_dict["effective_date"]=self.effective_date
		obj_as_dict["work_per_site"]=[{"location":w.location.loc_code,"productivity":w.location.productivity,"eligible_earnings":w.eligible_earnings,"vcp_percent":w.vcp_percent} for w in self.work_per_site]
		obj_as_dict["vcp_payout"]=self.vcp_payout
		return obj_as_dict

	
#LOCATIONS ENTITY
class Location:

	def __init__(self,loc_code,description,productivity,doubledown,pay_period):
		self.loc_code=loc_code
		self.description=description
		self.productivity=productivity
		self.doubledown=doubledown
		self.pay_period=pay_period


#WORKED HOURS 
class Work_Per_Site:

	def __init__(self,location,pay_period,worked_hours):
		self.location=location
		self.pay_period=pay_period
		self.worked_hours=worked_hours
		self.eligible_earnings=0
		self.vcp_percent=0


class Feedback:

	def __init__(self,feedback_type,pay_period):
		self.feedback_type=feedback_type
		self.pay_period=pay_period



class Attendance:

	def __init__(self,absence_instance,pay_period):
		self.absence_instance=absence_instance
		self.pay_period=pay_period















