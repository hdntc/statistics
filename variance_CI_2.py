import scipy.stats as stats
from csv import DictReader

# Reads from a csv file in the format value,frequency
# A confidence interval for the variance and std. deviation are found
# The data must be normally distributed because S^2(n-1)/var^2 ~ chi2 with n-1 d.f. iff the data is normal

def read_data(filename="data.csv") -> dict:
    result = {}
    with open(filename) as datafile:
        reader = DictReader(datafile)
        for row in reader:
            try:
                result[float(row["value"])] = float(row["frequency"])
            except(KeyError):
                result[float(row["value"])] = float(row["frequency"])
            except(ValueError):
                print("Error in data file - Values and frequencies must be convertable to float.")
                print(f"Erroneous row is {row}")
                return None
    return result

def get_sample_size(data:dict) -> float:
    """Given a frequnecy table {value:frequency}, find the sample size."""
    return sum(data.values())

def estimate_mean(data:dict) -> float:
    """Given a frequency table {value:frequency}, estimate the population mean."""
    """The sample mean is an unbiased estimator of the population mean."""
    return (1/get_sample_size(data)) * sum([value*freq for (value, freq) in data.items()])

def estimate_variance(data:dict) -> float:
    """Find an unbiased estimate of the population variance from a frequency table. This is s^2"""
    return (1/(get_sample_size(data)-1)) * (sum([(value**2 * freq) for (value,freq) in data.items()]) - get_sample_size(data) * estimate_mean(data)**2)

def estimate_std_dev(data:dict) -> float:
    """Find an unbiased estimate of the population standard deviation. This is s"""
    return (estimate_variance(data))**0.5

def find_variance_CI(data:dict, confidence_level:float) -> (float):
    n = get_sample_size(data)

    lower_bound = estimate_variance(data) * (n-1) / stats.chi2.isf(0.5 - confidence_level/200, n-1)
    upper_bound = estimate_variance(data) * (n-1) / stats.chi2.isf(0.5 + confidence_level/200, n-1)

    return (lower_bound, upper_bound)

def find_std_dev_CI(data:dict, confidence_level:float) -> (float):
    variance_CI = find_variance_CI(data, confidence_level)

    return (variance_CI[0]**0.5, variance_CI[1]**0.5)

def get_confidence() -> float:
    user_input = input("Enter confidence level (as a percentage):\n>>> ")
    try:
        float_value = float(user_input)
        if (float_value >= 100) or (float_value <= 0):
            print("The confidence level must range from 0 to 100 exclusive")
            return get_confidence()
        else:
            return float_value
    except(ValueError):
        print("Please enter a decimal number from 0 to 100 exclusive")
        return get_confidence()

if __name__ == "__main__":
    data = read_data()
    if data:
        print(f"Unbiased variance estimate {estimate_variance(data)}")
        print(f"Unbiased std. dev estimate {estimate_std_dev(data)}")
        print(f"Unbiased mean estimate {estimate_mean(data)}")
        
        confidence_level = get_confidence()
        print(f"Variance {confidence_level}% confidence interval: {find_variance_CI(data, confidence_level)}")
        print(f"Std. dev {confidence_level}% confidence interval: {find_std_dev_CI(data, confidence_level)}")
        
