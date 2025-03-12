import matplotlib
matplotlib.use('Agg')  # Fix for saving images in Flask backend

import matplotlib.pyplot as plt
import numpy as np
import os

def calculate_sip(monthly_investment, years, annual_return, annual_increase=0):
    """
    Calculate the final amount for a fixed SIP Investment.
    Also generates a graph showing SIP growth over time.

    :param monthly_investment: Fixed amount invested per month
    :param years: Duration of investment in years
    :param annual_return: Expected annual return on investment (in %)
    :param annual_increase: Annual increase in SIP amount (in %)
    :return: Dictionary containing final amount and graph URL
    """

    # Convert annual return percentage to decimal
    r = annual_return / 100
    n = 12
    t = years
    total_months = t * 12
    monthly_rate = r / n
    total_value = 0
    investment_timeline = []
    value_timeline = []

    current_sip = monthly_investment # starting with initial sip

    for month in range(1, total_months + 1):
        total_value = total_value * (1 + monthly_rate) + current_sip
        if month % 12 == 0: # every 12 months, increase sip
            current_sip += current_sip * (annual_increase / 100)
            investment_timeline.append(month / 12) # convert months to years
            value_timeline.append(round(total_value, 2))

    # Ensure the 'static' directory exists
    static_folder = "backend/static"
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    # Assign graph path before using it
    graph_path = os.path.join(static_folder, "sip_growth.png")

    print(f"Graph saved at: {graph_path}")
    
    # Plot the graph
    plt.figure(figsize=(10, 5))
    plt.plot(investment_timeline, value_timeline, marker='o', linestyle='-', color='b', label='SIP Growth')
    plt.xlabel('Years')
    plt.ylabel('Total Value (₹)')
    plt.title('SIP Growth Over Time')
    plt.legend()
    plt.grid(True)

    # Save the graph
    plt.savefig(graph_path)  
    plt.close()

    return {
        "final_amount": round(total_value, 2),
        "years": investment_timeline,
        "values": value_timeline,
    }

# Testing the function
if __name__ == "__main__":
    P = 10000  # Example: ₹10,000 monthly SIP
    T = 10  # Example: 10 years
    R = 12  # Example: 12% annual return rate
    increase = 10 #Example: SIP Increase by 10% annually

    result = calculate_sip(P, T, R, increase)
    print(f"Final Amount after {T} years of SIP of ₹{P} per month @ {R}% annual return: ₹{result}")
