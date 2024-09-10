from flask import Flask, request, jsonify
from solana.rpc.api import Client as SolanaClient
from solana.keypair import Keypair
import base64
import sqlite3

app = Flask(__name__)
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
solana_client = SolanaClient(SOLANA_RPC_URL)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY, 
                    username TEXT, 
                    public_key TEXT, 
                    secret_key TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Create a Solana Wallet for a User
def create_wallet(user_id, username):
    keypair = Keypair()
    public_key = keypair.public_key
    secret_key = base64.b64encode(keypair.secret_key).decode('utf-8')

    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (user_id, username, public_key, secret_key) VALUES (?, ?, ?, ?)",
              (user_id, username, str(public_key), secret_key))
    conn.commit()
    conn.close()

    return str(public_key), secret_key

@app.route('/api/create_wallet', methods=['POST'])
def create_wallet_endpoint():
    user_id = request.json.get('user_id')
    username = request.json.get('username')
    public_key, secret_key = create_wallet(user_id, username)

    return jsonify({
        "status": "success",
        "public_key": public_key,
        "secret_key": secret_key  # Handle this securely!
    })

@app.route('/api/get_balance', methods=['GET'])
def get_balance():
    public_key = request.args.get('public_key')
    balance = solana_client.get_balance(public_key)["result"]["value"] / 1e9  # Convert lamports to SOL
    return jsonify({"balance": balance})

if __name__ == '__main__':
    app.run(debug=True)
