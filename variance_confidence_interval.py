import scipy.stats as stats

# Given a set of data, find a confidence interval for the variance and std. deviation
# The data must be normally distributed.
# Relies on the fact that S^2(n-1)/v^2 follows a chi2 distribution with n-1 d.f. iff X ~ N
# stats.chi2.isf(p, df) returns the value of k such that P(X >= k) = 0.05

def estimate_population_variance(data : list) -> float:
    """Estimate the population variance from a list"""
    n = len(data)
    mean = sum(data)/n
    return (1/(n-1))*(sum([x**2 for x in data]) - n*mean**2)

def compute_var_bounds(variance_estimate, n, confidence):
    lower_bound = variance_estimate*(n-1)/stats.chi2.isf(0.5-confidence/200, n-1)
    upper_bound = variance_estimate*(n-1)/stats.chi2.isf(0.5+confidence/200, n-1)

    return (lower_bound, upper_bound)

def find_var_interval(data, confidence):
    n = len(data)

    return compute_var_bounds(estimate_population_variance(data), n, confidence)

def find_sd_interval(data, confidence):
    var_interval = find_var_interval(data, confidence)

    return (var_interval[0]**0.5, var_interval[1]**0.5)

def get_data() -> list:
    user_input = input("Enter data, which should be seperated by spaces:\n>>> ")
    if len(user_input) == 0:
        print("Please enter data")
        return get_data()
    else:
        split = user_input.split(" ")
        if len(split) == 1:
            print("There must be at least 2 data points")
            return get_data()
        else:
            try:
                values = [float(x) for x in split]
                return values
            except(ValueError):
                print("Please enter decimal values")
                return get_data()

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
    print("Your data must be normally distributed for this program to give valid results")
    while True:
        data = get_data()
        confidence = get_confidence()
        
        print(f"Population variance confidence interval at the {confidence}% level is {find_var_interval(data, confidence)}")
        print(f"Population standard deviation confidence interval at the {confidence}% level is {find_sd_interval(data, confidence)}")