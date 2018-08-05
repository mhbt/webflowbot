try:
    print("Somethis running")
    raise EnvironmentError
except:
    print("Error")

print("Hi this is me running again")