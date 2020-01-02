import requests
import json

data_dict = {
            "username"  	: "lasisi",
            "firstname" 	: "Inyang",
            "lastname"  	: "Kpongette",
            "email"     	: "inyangete@gmail.com",
            "phone"     	: "080316346306",
            "details"   	: "i am about to rule the world with python",
            "password"  	: "12345678"
        }

json_data = json.dumps(data_dict)

url = "http://localhost:8000/data/register/"

req = requests.post(url, json_data)

print(req.json())