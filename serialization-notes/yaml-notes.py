from pyaml import yaml

emp_dict = {"name": "John", "age": 45, "salary": 6000.0, "isMarried": True}

# Serialization to yaml string
yaml_string = yaml.dump(emp_dict)
print("Printing YAML string...")
print(yaml_string)

# Serialization to yaml file
with open("emp.yaml", "w") as f:
    yaml.dump(emp_dict, f)

# Deserialization from yaml string
e_dict = yaml.safe_load(yaml_string)
print("Printing deserialized YAML string...")
print(e_dict)

# Deserialization from yaml file
print("Printing deserialization from YAML file")
with open("emp.yaml", "r") as f:
    e_dict_f = yaml.safe_load(f)

print(e_dict_f)
