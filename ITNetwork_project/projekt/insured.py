class InsuredPerson:
    def __init__(self, name, surname, age, phone):
        self.name = name
        self.surname = surname
        self.age = age
        self.phone = phone

    def __str__(self):
        return f"pojištěnec {self.name} {self.surname}, Age: {self.age}, Phone: {self.phone}"
