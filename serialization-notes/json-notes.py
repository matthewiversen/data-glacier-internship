#
# * json.dump(obj, fileObj)    -returns nothing, goes to file
# * json.dumps(obj)            -returns string
# * json.load(obj, fileObj)    -returns nothing, goes to file
# * json.loads(obj)            -returns string

import json

employee = {
    "name": "John",
    "age": 55,
    "salary": 4000.0,
    "isMarried": True,
    "isHavingCar": None,
}

# serializing to string
json_string = json.dumps(employee, indent=4)
print(json_string)

# serializing to json file
with open("emp.json", "w") as f:
    json.dump(employee, f, indent=4)

# -------------------------------------------
json_string = """{
    "name": "durga",
    "age": 35,
    "salary": 1000.0,
    "isMarried": true,
    "isHavingCar": null
}"""

# deserializing from string
emp_dict = json.loads(json_string)
print(type(emp_dict))

for key, value in emp_dict.items():
    print(key, ":", value)
print()

# deserializing from json file
with open("emp.json", "r") as f:
    emp_dict = json.load(f)

print(type(emp_dict))

for key, value in emp_dict.items():
    print(key, ":", value)
