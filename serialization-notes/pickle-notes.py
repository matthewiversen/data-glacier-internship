#
# * pickle.dump(object, file)
# * pickle.load(file)

import pickle


class Employee:
    def __init__(self, eno, ename, esal, eaddr):
        self.eno = eno
        self.ename = ename
        self.esal = esal
        self.eaddr = eaddr

    def display(self):
        print(
            f"ENO: {self.eno}, ENAME: {self.ename}, ESAL: {self.esal}, EADDR: {self.eaddr}"
        )


emp = Employee(101, "John", 4500, "NYC")

# serializing
with open("emp.pkl", "wb") as f:
    pickle.dump(emp, f)
    print("Pickling complete")

# deserializing
with open("emp.pkl", "rb") as f:
    obj = pickle.load(f)
    print("Unpickling complete")
    obj.display()
