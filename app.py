from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# Initialize the Application.
app = Flask(__name__)
# Set base dir magic variable.
basedir = os.path.abspath(os.path.dirname(__file__))

# Setting up the Database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
# Set it to False otherwise it will give warning in console. In the future, that default will change to False.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the Database.
db = SQLAlchemy(app)
# Initialize  Marshmallow.
ma = Marshmallow(app)


# This is Consumption Class/Model.
class Consumption(db.Model):
    # SQLAlchemy ORM, needs there to be at least one column denoted as a primary key column.
    id = db.Column(db.Integer, primary_key=True)
    percentage_cpu_used = db.Column(db.Integer)       # CPU Used
    percentage_memory_used = db.Column(db.Integer)    # Memory Used

    # Define Initializer.
    def __init__(self, percentage_cpu_used, percentage_memory_used):
        self.percentage_cpu_used = percentage_cpu_used
        self.percentage_memory_used = percentage_memory_used


# Create Consumption Schema.
class ConsumptionSchema(ma.Schema):
    class Meta:
        # Define which all fields to show.
        fields = ('percentage_cpu_used', 'percentage_memory_used')


# Initialize the Schema.
consumption_schema = ConsumptionSchema()
consumptions_schema = ConsumptionSchema(many=True)    # Dealing with many items.


# Condition to check given Integer between 0-100.
def expectedrange(input1):
    if input1 in range(1, 100):
        return 200
    else:
        return 500


# This is the Metrics Ingestion Route.
@app.route('/metrics', methods=['POST'])
def ingest_metrics():
    percentage_cpu_used = request.json['percentage_cpu_used']
    percentage_memory_used = request.json['percentage_memory_used']

    if expectedrange(percentage_cpu_used) == 200 and expectedrange(percentage_memory_used) == 200:
        new_consumption = Consumption(percentage_cpu_used, percentage_memory_used)

        db.session.add(new_consumption)    # Adding Session.
        db.session.commit()                # Commit to the Database.

        return consumption_schema.jsonify(new_consumption), 200   # Returning 200 response if all OK.
    else:
        return "ERROR: Values should be between 0-100", 500       # Returning 500 response if something's WRONG.


# This is Report Generation Route.
@app.route('/report', methods=['GET'])
def generate_report():
    all_consumptions = Consumption.query.all()             # Get all the data.
    result = consumptions_schema.dump(all_consumptions)    # Dump all the data.
    for consumption in result:
        # Extract the sender's IP Address during the GET Request.
        consumption.update({"ip": str(request.remote_addr)})
    return jsonify(result), 200


# Generate the Database.
db.create_all()

# Run the Server.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
