#Rule - No content in brackets should be there in VOICE_ONLY column. 
'''
Example:  
To complete the Master Promissory Note (M.P.N) and entrance counseling, students must go to the Federal Student Aid website. ----- Incorrect 
To complete the Master Promissory Note and entrance counseling, students must go to the Federal Student Aid website. ------------- Correct.
'''
def no_content_in_brackets():
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile

	file_name="No_content_in_brackets.py"
	configFile = 'C:/Configuration.xlsx'
	rule=file_name[:file_name.find('.py')]
	file_directory= 'C:/uploads'

	print('hjcgweygcieskcbesabecacebjkscuabsjdkcje----------------------------------===============================')
	
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
				print('file-----------',file)
				print('f-----------',f)
				print('------------------',file.startswith(f))
				if(file.startswith(f)):
					files.append(file)

	regex = re.compile('[@!#$%^&*()<>?/\|}{~]')

	data=[]

	print('files---------------------',files)
		
	for file in files:
		df = pd.read_excel(file_directory+'/'+file)
		df.index = range(2,df.shape[0]+2)
		
		for index, row in df.iterrows():
			for column_name in columns_to_apply:
				column_value=row[column_name]
				if(type(column_value)!=float):
					if():
						#print(index)
						entry=[index,file,column_name+' has contents inside the brackets']
						print('The row ' + str(index) + ' in the file ' + file + ' has content inside brackets in the '+ column_name +' column')
						data.append(entry)
					
	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)