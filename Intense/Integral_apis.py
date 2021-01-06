import requests

# site_path = "https://tes.com.bd/"
site_path = "http://127.0.0.1:8000/"


# site_path = "https://tango99.herokuapp.com/"
#site_path = "http://128.199.66.61:8080/"

#site_path = "https://tango99.herokuapp.com/"
#site_path = "http://128.199.66.61:8080/"
#site_path = "https://tes.com.bd/"
#site_path = "http://128.199.114.154:8080/"

#site_path = "https://tango99.herokuapp.com/"
#site_path = "http://128.199.66.61:8080/"

def get_email_config():
    url = site_path+ "email/config_value"
    value = requests.get(url = url) 
    return (value.json())


def create_user_balance(data):
    url = site_path+ "user/balance/"
    requests.post(url = url,data = data) 
   
def create_user_profile(data):
    url = site_path + "user/create_profile/"
    requests.post(url = url,data = data) 

def create_product_code(data):
    url = site_path + "product/insert_value/"
    data=requests.post(url = url,data = data) 
    return data


def ratings(product_id):
	product_id=int(product_id)
	url = site_path+ "product/ratings/product_id/"
	value = requests.get(url = url) 
	return (value.json())


def product_data_upload(data):
    url = site_path + "product/upload/"
    data = requests.post(url = url,data = data) 
    return data

def category1_data_upload(data):
    url = site_path + "category/insert1/"
    data = requests.post(url = url,data = data) 
    return data


def category_data_upload(data):
    url = site_path + "category/insert/"
    data = requests.post(url = url,data = data) 
    return data

def product_image_data_upload(data):
    url = site_path + "product/insert_product_image/"
    data = requests.post(url = url,data = data) 
    return data

def product_price_data_upload(data):
    url = site_path + "productdetails/addprice/"
    data = requests.post(url = url,data = data) 
    return data

def product_specification_data_upload(data):
    url = site_path + "productdetails/addspec/"
    data = requests.post(url = url,data = data) 
    return data

def product_point_data_upload(data):
    url = site_path + "productdetails/addpoints/"
    data = requests.post(url = url,data = data) 
    return data

def product_discount_data_upload(data):
    url = site_path + "productdetails/insert_specific/"
    data = requests.post(url = url,data = data) 
    return data

def product_data_update(product_id, data):
    print("product er moddhe dhuktese")
    url = site_path + "product/update_product/" +str(product_id)+ "/"
    data = requests.post(url = url,data = data) 
    return data

def price_update(product_id, data):
    print("price er moddhe dhukse integral api")
    url = site_path + "productdetails/updateprice/" +str(product_id)+ "/"
    print(url)
    data = requests.post(url = url,data = data) 
    print(data)
    return data

def discount_data_update(product_id, data):
    url = site_path + "productdetails/specific_value/" +str(product_id)+ "/"
    data = requests.post(url = url,data = data) 
    return data

def point_data_update(product_id, data):
    url = site_path + "productdetails/updatepoints/" +str(product_id)+ "/"
    data = requests.post(url = url,data = data) 
    return data

def specification_data_update(product_id, data):
    url = site_path + "productdetails/updatespec/" +str(product_id)+ "/"
    data = requests.post(url = url,data = data)
    return data

def group_product_data_update(data):
    url = site_path + "product/group/create/"
    data = requests.post(url = url,data = data)
    return data

def group_product_data_modification(product_id, data):
    url = site_path + "edit_group_product/" +str(product_id)+ "/"
    #127.0.0.1:8000/product/group/edit/1
    data = requests.post(url = url,data = data)
    return data
    