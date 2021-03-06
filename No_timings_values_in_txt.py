#Rule 29 - There should not be any timing related information in TEXT, VOICE and VOICE_ONLY column of timing data file. Extra information about the service can be added in the DESCRIPTION column 
def no_timings_values_in_txt():
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

	file_name="No_timings_values_in_txt.py"
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

	for file in files:
		df = pd.read_excel(file_directory+'/'+file)
		df.index = range(2,df.shape[0]+2)

		for index, row in df.iterrows():
			for column_name in columns_to_apply:
				txt=row[column_name]
				if(type(txt)!=float):
					if(re.search(r"^(0[0-9]|1[0-9]|2[0-3]|[0-9]):[0-5][0-9]$", txt)):
						entry=[index,file,column_name+' has timings information in its contents']
						print('The row '+str(index)+' in the file '+file+' has timings in the '+column_name+' column')
						data.append(entry)

	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)