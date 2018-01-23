import requests
import os
os.environ.keys()

# web scraping
r = requests.get("http://github.com/adambard/learnxinyminutes-docs")
r.status_code
r.text
print(r.text)
os.getcwd()
f = open("learnxinyminutes.html", "wb")
f.write(r.text.encode("UTF-8"))
f.close()

# downloading a csv
fp = "https://raw.githubusercontent.com/adambard/learnxinyminutes-docs/master/"
fn = "pets.csv"
r = requests.get(fp + fn)
print(r.text)
f = open(fn, "wb")
f.write(r.text.encode("UTF-8"))
f.close()

# reading a csv
import pandas as pd
import numpy as np
import scipy as sp
pets = pd.read_csv(fn)
pets

# two different ways to print out a columns
pets.age
pets["age"]

pets.head(2) # prints first 2 rows
pets.tail(1) # prints last row

pets.name[1]
pets.species[0]
"{name} wants to eat {food}".format(name="Bob", food="lasagna")
