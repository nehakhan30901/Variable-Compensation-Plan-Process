import unittest
import Models
import Input

class TestModels():

	def test_employee(self):
		try:
			emp=Models.Employee(9,"Neha Khan","Hourly","P","P03232","1112","USA","Active",13.5,0.5,"30-Nov-2015")
			self.assertEqual(emp.empl_id,9)
			self.assertEqual(emp.empl_name,"Neha Khan")
		except:
			raise	

			
	def test_location(self):
		try:
			loc=Models.Location("SEA8","Seattle Port 99",0.5,0.0,"30-Nov-2015")
			self.assertEqual(loc.loc_code,"SEA8")
			self.assertEqual(loc.description,"Seattle Port 99")
		except:
			raise
	
class TestInputs(unittest.TestCase):

	def test_load_attendance_data(self):
		pay_period=("01-Nov-2015","30-Nov-2015")
		att=Input.load_attendance("/Users/nehakhan/Documents/Global_VCP_Program/Data/Attendance.csv",pay_period)
		for key in att:
			print(key,att[key])
			self.assertFalse[att[key].absence_instance==-1]

	def test_load_locations_data(self):
		pay_period=("01-Nov-2015","30-Nov-2015")
		locations=Input.load_location_data("/Users/nehakhan/Documents/Global_VCP_Program/Data/Locations.csv",pay_period)


if __name__ == '__main__':
    unittest.main()