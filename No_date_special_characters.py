#Rule - No date, special character, URL should be there in VOICE & VOICE_ONLY column(s) – Alphabets & Numbers only.
def No_date_special_characters():
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile
	from dateutil.parser import parse
	import validators

	file_name="No_date_special_characters.py"
	configFile = 'C:/Configuration.xlsx'
	rule=file_name[:file_name.find('.py')]
	file_directory= 'C:/uploads'
	
	config_file=configFile
	target= 'C:/Users/105666/projects/pythonProject/angular-python-flask-demo/DataFiles_Rules_Report.xlsx'
	all_files=os.listdir(file_directory)
	files=[]

	config=pd.read_excel(config_file)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	columns_to_apply=to_check['columns_to_apply']

	if(to_check['files_to_apply']=='ALL'):
		files = all_files
	else:
		for f in files_to_apply:
			for file in all_files:
				if(file.startswith(f)):
					files.append(file) 

	data=[]

	regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')

	def has_date(string,fuzzy=False):
		try: 
			parse(string, fuzzy=fuzzy)
			return True
		except ValueError:
			return False

	def has_url(string):
		url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
		return url
		
	data=[]

	for file in files:
		df = pd.read_excel(file_directory+'/'+file)
		df.index = range(2,df.shape[0]+2)

		for index, row in df.iterrows():
			for column_name in columns_to_apply:
				column_value=row[column_name]
				if(type(column_value)!=float):
					if(has_date(column_value)):
						#print(index)
						entry=[index,file,column_name+' has date']
						print('The row '+str(index)+' in the file '+file+' has date in the '+column_name+' column')
						data.append(entry)
					if(regex.search(column_value) != None):
						entry=[index,file,column_name+' has special characters']
						print('The row '+str(index)+' in the file '+file+' has special characters in the '+column_name+' column')
						data.append(entry)
					if(has_url(column_value)):
						#print(index)
						entry=[index,file,column_name+' has url in its contents']
						print('The row '+str(index)+' in the file '+file+' has url in the '+column_name+' column')
						data.append(entry)
					
	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)