import matplotlib 

matplotlib.use('Agg') # to avoid any issues with backend

import matplotlib.pyplot as plt, numpy as np
import os

def calculate_sip(monthly_investment, years, annual_return):
    """
    Calculate the final amount for a fixed SIP Investment.
    Also generates a graph showing SIP growth over time.

    :param monthly_investment: Fixed amount invested per month
    :param years: Duration of investment in years
    :param annual_return: Expected annual return on investment (in %)
    :return: Final corpus (Total value of investment)
    """

    # convert annual return percentage to decimal
    r = annual_return / 100
    n = 12
    t = years

    # sip formula
    total_months = t * 12
    monthly_rate = r / n
    total_value = 0
    investment_timeline = []
    value_timeline = []

    for month in range (1, total_months + 1):
        total_value = total_value * (1 + monthly_rate) + monthly_investment
        if month % 12 == 0:
            investment_timeline.append(month / 12)
            value_timeline.append(total_value)

    # ensuring the 'static' directory exists
    if not os.path.exists("backend/static"):
        os.makedirs("backend/static")
    
    # plot the graph

    plt.figure(figsize=(10, 5)) 
    plt.plot(investment_timeline, value_timeline, marker='o', linestyle='-', color='b', label='SIP Growth')
    plt.xlabel('Years')
    plt.ylabel('Total Value')
    plt.title('SIP Growth Over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig("backend/static/sip_growth.png") # saving graph as image
    plt.close()

    return round(total_value, 2)

# testing the function

if __name__ == "__main__":
    P = 10000 # example: 10000 monthly SIP
    T = 10 # example: 10 years
    R = 12 # example: 12% annual return rate

    result = calculate_sip(P, T, R)
    print(f"Final Amount after {T} years of SIP of {P} per month @ {R}% annual return: {result}")