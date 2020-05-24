import numpy
import csv
from scipy.stats import norm
from analyser import estimate_std_dev, estimate_mean

# Two vectors with the same random length R are generated. They are attached from the origin 
# and have an angle theta between them. Calculate the expected area of the triangle enclosed
# R ~ U(0, r)
# theta ~ U(0, pi)
# Is this value different to r^2 / 3pi ??

def generate_R(r):
    return numpy.random.uniform(0, r)

def generate_theta():
    return numpy.random.uniform(0, numpy.pi)

def generate_area(r):
    return 0.5 * numpy.sin(generate_theta()) * generate_R(r)**2

def generate_multiple_areas(r,n):
    return {generate_area(r) : 1 for _ in range(n)} #frequency table

def update_data(r):
    values =  [[generate_area(r), 1] for _ in range(1000)]
    with open("data.csv", "a", newline="") as datafile:
        writer = csv.writer(datafile)
        for row in values:
            writer.writerow(row)

if __name__ == "__main__":
    values = generate_multiple_areas(10, 1000000)
    s = estimate_std_dev(values)
    xbar = estimate_mean(values)
    z = (xbar - (10**2 / (3*numpy.pi))) / (s / 1000000**0.5)
    print(f"Test statistic is {z}")
    print(f"P(Z<=z) = {norm.cdf(z, 0, 1)}\nP(Z>=z) = {norm.sf(z, 0, 1)}")
