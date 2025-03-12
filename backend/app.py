import yfinance as yf
from flask import Flask, request, jsonify, render_template
from sip_calculator import calculate_sip
import os

# Debug info
print("Template Folder Path:", os.path.abspath("backend/templates"))

app = Flask(__name__, template_folder=os.path.abspath("backend/templates"), 
            static_folder=os.path.abspath("backend/static"), static_url_path='/static')

@app.route('/')
def home():
    """ Serve the landing page """
    try:
        return render_template('landing.html')
    except Exception as e:
        return jsonify({"error": f"Template Error: {str(e)}"}), 500

@app.route('/calculator')
def calculator():
    """ Serve the calculator page """
    return render_template('calculator.html')

# Debugging route: list all registered routes
@app.route('/routes', methods=['GET'])
def list_routes():
    """ List all registered routes (for debugging). """
    output = []
    for rule in app.url_map.iter_rules():
        output.append(str(rule))
    return jsonify({"routes": output})

@app.route('/calculate_sip', methods=['POST'])
def sip_route():
    """
    API route to calculate SIP returns.
    Expects JSON input with 'monthly_investment', 'years', 'annual_return', 'annual_increase'.
    """

    data = request.get_json()

    # Extract values
    monthly_investment = data.get('monthly_investment', 0)
    years = data.get('years', 0)
    annual_return = data.get('annual_return', 0)
    annual_increase = data.get('annual_increase', 0)

    # Validate input
    if not all([monthly_investment, years, annual_return]):
        return jsonify({"error": "Invalid Input. Please provide 'monthly_investment', 'years', and 'annual_return'."}), 400
    
    # Calculate SIP and get data points
    result = calculate_sip(monthly_investment, years, annual_return, annual_increase)

    return jsonify(result)

@app.route('/market_trends')
def market_trends():
    """ Serve the market trends page """
    return render_template('market_trends.html')

@app.route('/market_trend_graph')
def get_market_trend_graph():
    """Fetch live market data for NIFTY 50 or other indices from last 30 days"""
    ticker = "^NSEI" # nifty 50 index

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo") # data for last 30 days
 
        if hist.empty:
            return jsonify({"error": "Market Data Unavailable."}), 500
        
        dates = hist.index.strftime("%Y-%m-%d").tolist()
        prices = hist["Close"].round(2).tolist()

        return jsonify({"dates": dates, "prices": prices})
    
    except Exception as e:
        print(f"Error fetching market data: {str(e)}")  # Debugging print statement
        return jsonify({"error": f"Failed to fetch market data: {str(e)}"}), 500
    
@app.route('/market_data')
def get_market_data():
    """ Fetch live market data for Nifty 50 (or other indices) """
    ticker = "^NSEI"  # Nifty 50 index
    
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")

        if hist.empty:
            return jsonify({"error": "Market data not available"}), 500

        latest_data = hist.iloc[-1]  # Get the latest available row
        return jsonify({
            "date": latest_data.name.strftime('%Y-%m-%d'),
            "open": round(latest_data["Open"], 2),
            "high": round(latest_data["High"], 2),
            "low": round(latest_data["Low"], 2),
            "close": round(latest_data["Close"], 2)
        })
    except Exception as e:
        print(f"Error fetching live market data: {str(e)}")  # Debugging print statement
        return jsonify({"error": f"Failed to fetch live market data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
