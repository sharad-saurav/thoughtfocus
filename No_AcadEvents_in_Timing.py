#Rule 28 - Make sure interactions in AcadEvents are not present in Timing file.
def no_acadEvents_in_timing():
	import re
	import os
	import sys
	import json
	import pandas as pd
	import openpyxl
	from pandas import ExcelWriter
	from pandas import ExcelFile
	import validators
	
	configFile = 'C:/Configuration.xlsx'
	file_name='No_AcadEvents_in_Timing.py'
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
			column_value=row['ENTITY_TYPE']
			if(type(column_value)!=float):
				if(column_value=='AcadEvents'):
					entry=[index,file,column_name+' has entity of type AcadEvents which is not allowed entity type in timing file']
					print('The row '+str(index)+' in the file '+file+' is of type AcadEvents which is not allowed')
					data.append(entry)

	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)