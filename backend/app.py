from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
from sip_calculator import calculate_sip
import os

# Print debug info
print("Template Folder Path:", os.path.abspath("backend/templates"))

app = Flask(__name__, template_folder=os.path.abspath("backend/templates"), 
            static_folder=os.path.abspath("backend/static"), static_url_path='/static')

@app.route('/')
def home():
    try:
        return render_template('landing.html')  # Serve the landing page
    except Exception as e:
        return jsonify({"error": f"Template Error: {str(e)}"}), 500

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')  # Calculator page

# Debugging route: list all registered routes
@app.route('/routes', methods=['GET'])
def list_routes():
    """List all registered routes (for debugging)."""
    output = []
    for rule in app.url_map.iter_rules():
        output.append(str(rule))
    return jsonify({"routes": output})

@app.route('/calculate_sip', methods=['POST'])
def sip_route():
    """
    API route to calculate SIP returns.
    Expects JSON input with 'monthly_investment', 'years', 'annual_return', 'annual_increase.
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
    
    # Calculate SIP
    final_amount = calculate_sip(monthly_investment, years, annual_return, annual_increase)  

    return jsonify({
        "final_amount": final_amount, 
        "graph_url": "http://127.0.0.1:5000/sip_graph"
    })

@app.route('/sip_graph')
def serve_sip_graph():
    """Returns the generated SIP Growth graph."""
    
    graph_path = os.path.join(app.static_folder, "sip_growth.png")

    if not os.path.exists(graph_path):
        return jsonify({"error": "Graph not found. Please run a SIP calculation first."}), 404
    
    return send_file(graph_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
