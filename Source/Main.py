import Models
import Input
import json
import PolicyFactory
import Output


def main():

	#Input
	config=Input.load_config("appconfig.yaml")
	employee_list=Input.generate_employee_data(config,Input.get_current_payperiod())
	
	#Process
	for employee in employee_list:
		employee.process_employee_vcp()

	#Output
	print(Output.serialize(employee_list))
	Output.save_to_db(config["db_setting"],employee_list)
		
			 

if __name__=="__main__":
	main() 