def PasswordChecker():
    password = input("Please enter your password: ")
    uppercase = False
    lowercase = False
    special = False
    numbers = False
    points = 0
    special_chars = "!@#$%^&*()-_=+[]|;:'\",.<>?/\\`~"
    common = False
    commonwords = ["admin", "password", "123456"]

    for i in password:
        if i.isupper():
            uppercase = True
        if i.islower():
            lowercase = True
        if i.isdigit():
            numbers = True
        if i in special_chars:
            special = True
    for j in commonwords:
        if j in password.lower():
            common = True
    if uppercase:
        points += 1
    if lowercase:
        points += 1
    if numbers:
        points += 1
    if special:
        points += 1
    if common:
        points -= 2
    if 8 <= len(password) <= 11:
        points += 1
    if len(password) >= 12:
        points += 2
    if points <= 0:
        print("Your password is weak.")
    elif 1 <= points <= 3:
        print("Your password is average.")
    else:  
        print("Your password is strong.")
    print("Score:", points)
