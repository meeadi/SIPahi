import matplotlib
matplotlib.use('Agg')  # Fix for saving images in Flask backend

import matplotlib.pyplot as plt
import numpy as np
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

    # Convert annual return percentage to decimal
    r = annual_return / 100
    n = 12
    t = years

    # SIP formula
    total_months = t * 12
    monthly_rate = r / n
    total_value = 0
    investment_timeline = []
    value_timeline = []

    for month in range(1, total_months + 1):
        total_value = total_value * (1 + monthly_rate) + monthly_investment
        if month % 12 == 0:
            investment_timeline.append(month / 12)  # Convert months to years
            value_timeline.append(total_value)

    # Ensure the 'static' directory exists
    static_folder = "backend/static"
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    graph_path = os.path.join(static_folder, "sip_growth.png")
    plt.savefig(graph_path)  # Save the graph
    plt.close()
    
    # Plot the graph
    plt.figure(figsize=(10, 5))
    plt.plot(investment_timeline, value_timeline, marker='o', linestyle='-', color='b', label='SIP Growth')
    plt.xlabel('Years')
    plt.ylabel('Total Value (₹)')
    plt.title('SIP Growth Over Time')
    plt.legend()
    plt.grid(True)

    # Save the graph
    graph_path = os.path.join(static_folder, "sip_growth.png")
    plt.savefig(graph_path)  
    plt.close()

    return round(total_value, 2)

# Testing the function
if __name__ == "__main__":
    P = 10000  # Example: ₹10,000 monthly SIP
    T = 10  # Example: 10 years
    R = 12  # Example: 12% annual return rate

    result = calculate_sip(P, T, R)
    print(f"Final Amount after {T} years of SIP of ₹{P} per month @ {R}% annual return: ₹{result}")
