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
pets["weight"][2]

pets.age[0:2] # in R, you would expect to get 3 rows doing this, but here you get 2:

# Charts
# matplotlib does data visualization in Python
import matplotlib as mpl
import matplotlib .pyplot as plt
%matplotlib inline

plt.hist(pets.age);

plt.boxplot(pets.weight);

plt.scatter(pets.age, pets.weight)
plt.xlabel("age")
plt.ylabel("weight")
plt.title("Pets");

# seaborn sits atop matplotlib and makes plots prettier
import seaborn as sns

plt.scatter(pets.age, pets.weight)
plt.xlabel("age")
plt.ylabel("weight")
plt.title("Pets");

# seaborn-specific plotting
sns.barplot(pets["age"])

# 4. Simple data cleaning and exploratory analysis ====

 #    Here's a more complicated example that demonstrates a basic data
 #    cleaning workflow leading to the creation of some exploratory plots
 #    and the running of a linear regression.
 #        The data set was transcribed from Wikipedia by hand. It contains
 #    all the Holy Roman Emperors and the important milestones in their lives
 #    (birth, death, coronation, etc.).
 #        The goal of the analysis will be to explore whether a relationship
 #    exists between emperor birth year and emperor lifespan.
 #    data source: https://en.wikipedia.org/wiki/Holy_Roman_Emperor

# load some data on Holy Roman Emperors
url = "https://raw.githubusercontent.com/e99n09/R-notes/master/data/hre.csv"
r = requests.get(url)
fp = "hre.csv"
with open(fp, "wb") as f:
    f.write(r.text.encode("UTF-8"))

hre = pd.read_csv(fp)

hre.head()


# Miscellaneous
"{name} wants to eat {food}".format(name="Bob", food="lasagna")
