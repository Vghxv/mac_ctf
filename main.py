import os
import random
import hmac
import hashlib
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

N = 128  # Key size in bits
BLOCK_SIZE = N // 4  # Block size in bits
FIXED_R = os.urandom(BLOCK_SIZE // 8)  # Fixed r of size n/4 bits
query_list = []

# Secret key generation
def Gen():
    return os.urandom(N // 8)  # N bits converted to bytes

def Mac_prime(k, m):
    # Simple HMAC with SHA256 for fixed-length input
    return hmac.new(k, m, hashlib.sha256).digest()

def Vulnerable_Mac(k, m):
    # Parse message into blocks of size BLOCK_SIZE bits
    m_bits = ''.join(f'{byte:08b}' for byte in m)
    blocks = [m_bits[i:i+BLOCK_SIZE] for i in range(0, len(m_bits), BLOCK_SIZE)]

    # Pad the last block with zeros if necessary
    if len(blocks[-1]) < BLOCK_SIZE:
        blocks[-1] = blocks[-1].ljust(BLOCK_SIZE, '0')

    d = len(blocks)  # Number of blocks
    t_list = [FIXED_R]
    for i, block in enumerate(blocks, start=1):
        # Prepare inputs: r || i || m_i
        # Convert i to its binary representation
        i_bin = i.to_bytes(BLOCK_SIZE // 8, byteorder='big')
        # Convert block from binary string to bytes
        m_i = int(block, 2).to_bytes(BLOCK_SIZE // 8, byteorder='big')
        # Compute t_i
        t_i_input = FIXED_R + i_bin + m_i  # Note: 'l' is omitted here
        t_i = Mac_prime(k, t_i_input)
        t_list.append(t_i)
    return t_list  # Output is (r, t_1, ..., t_d)

def unforgeable_Mac(k, m):
    # Parse message into blocks of size BLOCK_SIZE bits
    m_bits = ''.join(f'{byte:08b}' for byte in m)
    blocks = [m_bits[i:i+BLOCK_SIZE] for i in range(0, len(m_bits), BLOCK_SIZE)]
    if len(blocks[-1]) < BLOCK_SIZE:
        blocks[-1] = blocks[-1].ljust(BLOCK_SIZE, '0')
    d = len(blocks)  # Number of blocks
    l = len(m).to_bytes(BLOCK_SIZE // 8, byteorder='big')
    t_list = [FIXED_R]
    for i, block in enumerate(blocks, start=1):
        # Prepare inputs: r || l || i || m_i
        # Convert i to its binary representation
        i_bin = i.to_bytes(BLOCK_SIZE // 8, byteorder='big')
        # Convert block from binary string to bytes
        m_i = int(block, 2).to_bytes(BLOCK_SIZE // 8, byteorder='big')
        # Compute t_i with l
        t_i_input = FIXED_R + l + i_bin + m_i
        t_i = Mac_prime(k, t_i_input)
        t_list.append(t_i)
    return t_list  # Output is (r, t_1, ..., t_d)

def Verify_Mac(k, m, t_list):
    computed_t_list = Vulnerable_Mac(k, m)
    return t_list == computed_t_list



# Oracle endpoint
@app.route('/mac', methods=['POST'])
def mac_oracle():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Please provide a message in the request body.'}), 400

    message = data['message']
    if not isinstance(message, str):
        return jsonify({'error': 'Message must be a string.'}), 400

    m = message.encode()

    t_list = Vulnerable_Mac(SECRET_KEY, m)

    mac_hex = [r.hex() for r in t_list]
    query_list.append(message)
    return jsonify({'mac': mac_hex})

# Submission endpoint
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data or 'mac' not in data or not data['mac']:
        return jsonify({'error': 'Please provide a MAC in the request body.'}), 400
    mac_hex = data['mac']
    if not isinstance(mac_hex, list):
        return jsonify({'error': 'MAC must be a list of hex strings.'}), 400
    message = data['message']
    if not isinstance(message, str):
        return jsonify({'error': 'Message must be a string.'}), 400
    if message in query_list:
        return jsonify({'error': 'The message has already been queried.'}), 400
    message = message.encode()
    # Convert MAC components back to bytes
    try:
        t_list = [bytes.fromhex(t) for t in mac_hex]
    except ValueError:
        return jsonify({'error': 'Invalid hex in MAC components.'}), 400
    # Verify the MAC against the target message
    if Verify_Mac(SECRET_KEY, message, t_list):
        return jsonify({'result': 'Success! Here is your flag: ' + FLAG})
    else:
        return jsonify({'result': 'Invalid MAC. Try again.'})

# Instructions endpoint
@app.route('/', methods=['GET'])
def instructions():
    return render_template('instructions.html')

FLAG = "FLAG{y0u_h4v3_f0rg3d_4_v4l1d_m4c}"
SECRET_KEY = Gen()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)