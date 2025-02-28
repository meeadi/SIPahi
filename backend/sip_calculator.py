def calculate_sip(monthly_investment, years, annual_return):
    """
    Calculate the final amount for a fixed SIP Investment.

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
    final_amount = monthly_investment * ((1 + r / n) ** (n * t) - 1) / (r / n) * (1 + r / n)

    return round(final_amount, 2)

# testing the function

if __name__ == "__main__":
    P = 10000 # example: 10000 monthly SIP
    T = 10 # example: 10 years
    R = 12 # example: 12% annual return rate

    result = calculate_sip(P, T, R)
    print(f"Final Amount after {T} years of SIP of {P} per month @ {R}% annual return: {result}")