import re

check = True
email = input("E-mail (Username): ")
while check:
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        check = False
    else:
        email = input("Invalid E-mail. Please re-enter: ")

firstname = input("First Name: ")
lastname = input("Last Name: ")
accountsince = input("Account Since: ")

print("You entered: "
      "\nEmail: " + email +
      "\nFirst Name: " + firstname +
      "\nLast Name: " + lastname +
      "\nAccount Since: " + accountsince)