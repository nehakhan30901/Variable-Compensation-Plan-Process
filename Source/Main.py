import Models
import Input
import json
import PolicyFactory
import Output
import marshal


def main():

	config=Input.load_config("appconfig.yaml")

	employee_list=Input.generate_employee_data(config,Input.get_current_payperiod())
	
	for employee in employee_list:
		employee.process_employee_vcp()
		print(Output.serialize(employee))
		#print ("\nEmployee name :"+ employee.empl_name+"\nVCP policy :"+employee.vcp_policy.policy_type+"\nCalculated payout "+str(employee.vcp_payout))
		#print ("--------------------------------------------------")
			 

if __name__=="__main__":
	main() 