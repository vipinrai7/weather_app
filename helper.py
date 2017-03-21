
def data_dict(data):
	my_dict={}
	my_dict['name']=str(data['name'])
	my_dict['description']=str(data['weather'][0]['description'])
	my_dict['data']=data['main']
	my_dict['wind']=data['wind']
	return my_dict