#Rule 14 - We should not construct an interaction of Primary + Secondary (without keyword) 
def rule_missing_keyword():
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile

	file_name="Check_for_missing_Keyword.py"
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

		newdf=df[df.duplicated(columns_to_apply)]
		for index,row in newdf.iterrows():
			entity_name=newdf['ENTITY_NAME']
			secondary_entity_name=newdf['SECONDARY_ENTITY_NAME']
			keyword=newdf['KEYWORD']
			if(type(entity_name)!=float and type(secondary_entity_name)!=float):
				if(type(keyword)==float):
					entry=[index,file,'The '+entity_name+' + '+secondary_entity_name+' is an entity interaction of (Primary Entity + Secondary Entity) without Keyword']
					print('The row '+str(index)+'in the file '+file+' has an interaction of Primary Entity + Secondary Entity without Keyword')
					data.append(entry)
					
	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)