from flask import Flask, jsonify, request
import threading
from pyraft import raft
import telnetlib
import time
from datetime import datetime
#from records_structure import records_store


app = Flask(__name__)

# Create a Raft node
node = raft.make_default_node()

#node.data = records_store

# Function to start Flask app on a separate thread
def start_flask_app(port):
    app.run(port=port)

# Define a function to start Flask app on the given port
def start_flask_app_on_port(port):
    flask_thread = threading.Thread(target=start_flask_app, args=(port,))
    flask_thread.start()

# Set up Flask server on a separate thread when a node starts
def on_start_handler(node):
    start_flask_app_on_port(8050)  # Change the port as needed

# Register on_start_handler for the on_start event
node.worker.handler['on_start'] = on_start_handler


#process Data



def process_register_broker_data(data, bId):
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(0.5)

    # Create a Telnet connection
    tn = telnetlib.Telnet('localhost', 5020)

    # Store the broker record
    for key, value in data.items():
        command = f"set RegisterBrokerRecord.{bId}.{key} {value}"
        print(command)  # Print the command being sent
        tn.write(command.encode('ascii') + b'\r\n')
        time.sleep(0.1)

    # Introduce a delay after sending other commands
    time.sleep(0.1)

    command_1 = f"set RegisterBrokerRecord.{bId}.timestamp {current_timestamp}"
    tn.write(command_1.encode('ascii') + b'\r\n')

    # Close the Telnet connection
    tn.close()


def process_create_topic_name(data, tname):
    # Get the current timestamp
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add the timestamp to the data
    data['timestamp'] = current_timestamp

    # Create a Telnet connection
    tn = telnetlib.Telnet('localhost', 5020)

    # Store the broker record
    for key, value in data.items():
        command = f"set TopicRecord.{tname}.{key} {value}"
        print(command)  # Print the command being sent
        tn.write(command.encode('ascii') + b'\r\n')
        time.sleep(0.1)


    # Close the Telnet connection
    tn.close()

def process_create_partition(data,pid):
     # Get the current timestamp
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add the timestamp to the data
    data['timestamp'] = current_timestamp
    # Create a Telnet connection
    tn = telnetlib.Telnet('localhost', 5020)

    # Store the broker record
    for key, value in data.items():
        command = f"set PartitionRecord.{pid}.{key} {value}"
        tn.write(command.encode('ascii') + b'\r\n')
        time.sleep(0.1)
        
    # Close the Telnet connection
    tn.close()

def process_create_producer(data,prid,broker_id,broker_epoch):
     # Get the current timestamp
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add the timestamp to the data
    data['timestamp'] = current_timestamp
    # Create a Telnet connection
    tn = telnetlib.Telnet('localhost', 5020)




    command_1 = f"set ProducerRecord.{prid}.brokerId {broker_id}"
    command_2 = f"set ProducerRecord.{prid}.brokerEpoch {broker_epoch}"
    command_3 = f"set ProducerRecord.{prid}.producerId {prid}"

    # Write commands to the Telnet connection
    tn.write(command_1.encode('ascii') + b'\r\n')
    tn.write(command_2.encode('ascii') + b'\r\n')
    tn.write(command_3.encode('ascii') + b'\r\n')

	# Close the Telnet connection
    tn.close()



# Define a route to get the Raft node's status
@app.route('/status', methods=['GET'])
def get_status():
    status = {'node_id': node.nid, 'state': node.state}
    return jsonify(status)

# Define a route to store key-value pairs
@app.route('/store', methods=['POST'])
def store_data():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')

    if key and value:
        # Perform storage operation in your Raft node or data store
        # For example:
        # node.set(key, value)
        return jsonify({'message': f'Key-value pair ({key}: {value}) stored successfully'})
    else:
        return jsonify({'error': 'Invalid data provided'})

# Define a route to retrieve a value for a given key
@app.route('/retrieve/<key>', methods=['GET'])
def retrieve_data(key):
    # Retrieve data based on the key from your Raft node or data store
    # For example:
    # value = node.get(key)
    value = 'some_value'  # Replace this with actual retrieval logic
    if value:
        return jsonify({'key': key, 'value': value})
    else:
        return jsonify({'error': 'Key not found'})
    

@app.route('/register_broker', methods=['POST'])
def register_broker():
    data = request.get_json()
    bId = data['brokerId']
    if data:
    
        process_register_broker_data(data,bId)
        return jsonify({'message': 'Broker registered successfully'})
    else:
        return jsonify({'error': 'Invalid data provided'})
        
@app.route('/create_topic', methods=['POST'])
def create_topic():
    data = request.get_json()
    tname = data['name']
    if data:
    
        process_create_topic_name(data,tname)
        return jsonify({'message': 'Topic registered successfully'})
    else:
        return jsonify({'error': 'Invalid data provided'})
        
@app.route('/create_partition', methods=['POST'])
def create_partition():
    data = request.get_json()
    pid = data['partitionId']
    if data:
    
        process_create_partition(data,pid)
        return jsonify({'message': 'Producer Created successfully'})
    else:
        return jsonify({'error': 'Invalid data provided'})
        



def get_unique_broker_ids():
    broker_ids = set()
    for key in node.data:
        if key.startswith('RegisterBrokerRecord.'):
            parts = key.split('.')
            if len(parts) > 1:
                broker_id = parts[1]
                broker_ids.add(broker_id)
    return list(broker_ids)

# Route to get all active brokers
@app.route('/get_all_active_brokers', methods=['GET'])
def get_all_active_brokers():
    unique_broker_ids = get_unique_broker_ids()
    return jsonify({'active_brokers': unique_broker_ids})
    


def get_records_by_broker_id(broker_id):
    prefix = f"RegisterBrokerRecord.{broker_id}."
    matching_records = {}
    
    for key, value in node.data.items():
        if key.startswith(prefix):
            new_key = key[len(prefix):]  # Extract the part after the prefix
            matching_records[new_key] = value
    
    return matching_records

def get_records_by_topic_name(tname):
    prefix = f"TopicRecord.{tname}."
    matching_records = {}
    
    for key, value in node.data.items():
        if key.startswith(prefix):
            new_key = key[len(prefix):]  # Extract the part after the prefix
            matching_records[new_key] = value
    
    return matching_records
    
@app.route('/create_producer/<broker_id>/<broker_epoch>', methods=['POST'])
def create_producer(broker_id,broker_epoch):
    data = request.get_json()
    prid = data['producerId']
    if data:
    
        process_create_producer(data,prid,broker_id,broker_epoch)
        return jsonify({'message': 'Partition Created successfully'})
    else:
        return jsonify({'error': 'Invalid data provided'})

   

# Route to get broker details by ID
@app.route('/get_broker_by_id/<broker_id>', methods=['GET'])
def get_broker_details(broker_id):
    broker_details = get_records_by_broker_id(broker_id)
    return jsonify(broker_details)

@app.route('/get_topic_by_name/<tname>', methods=['GET'])
def get_topic_details(tname):
    topic_details = get_records_by_topic_name(tname)
    return jsonify(topic_details)  

   
@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    return jsonify(node.data)

# Start the Raft node
node.start()
node.join()
