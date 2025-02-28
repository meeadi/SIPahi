from flask import Flask, request, jsonify
from sip_calculator import calculate_sip

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>SIPahi Flask API is Running!</h1><p>Use the <code>/calculate_sip</code> endpoint to calculate SIP returns.</p>"

# Debugging route: list all registered routes
@app.route('/routes', methods=['GET'])
def list_routes():
    """List all registered routes(for debugging)."""

    output = []
    for rule in app.url_map.iter_rules():
        output.append(str(rule))
    return jsonify({"routes": output})

@app.route('/calculate_sip', methods=['POST'])
def sip_route():
    """
    API route to calculate SIP returns.
    Expects JSON input with 'monthly_investment', 'years', 'annual_return'.
    """

    data = request.get_json()

    # extract values
    monthly_investment = data.get('monthly_investment', 0)
    years = data.get('years', 0)
    annual_return = data.get('annual_return', 0)

    # validate input
    if not all([monthly_investment, years, annual_return]):
        return jsonify({"error": "Invalid Input. Please provide 'monthly_investment', 'years', 'annual_return'."}), 400
    
    # calculate SIP
    final_amount = calculate_sip(monthly_investment, years, annual_return)  

    return jsonify({"final_amount": final_amount})

if __name__ == '__main__':
    app.run(debug=True)