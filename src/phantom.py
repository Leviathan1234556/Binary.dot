from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.transaction import Transaction, TransactionInstruction
from solana.publickey import PublicKey

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/transfer', methods=['POST'])
def transfer():
    amount = request.form.get('amount')
    recipient = request.form.get('recipient')

    # Validate amount and recipient
    if not amount or not recipient:
        return jsonify({'error': 'Amount and recipient address are required.'}), 400

    # Convert amount to lamports (1 SOL = 10^9 lamports)
    amount_lamports = int(float(amount) * 10**9)

    # Create a new Solana keypair
    wallet = Keypair()
    sender_address = wallet.public_key

    # Create Solana client
    client = Client("https://api.devnet.solana.com")

    # Create a new transaction
    transaction = Transaction()

    # Add a transfer instruction to the transaction
    transfer_instruction = TransactionInstruction(
        keys=[
            {
                'pubkey': sender_address,
                'is_signer': True,
                'is_writable': True
            },
            {
                'pubkey': PublicKey(recipient),
                'is_signer': False,
                'is_writable': True
            }
        ],
        program_id="system_program_id",  # Replace with the actual program ID
        data=b'some_data'
    )

    # Add the transfer instruction to the transaction
    transaction.add(transfer_instruction)

    # Sign the transaction
    transaction.sign(wallet)

    # Send the transaction
    try:
        tx_hash = client.send_transaction(transaction)
        return jsonify({'message': 'Transaction sent successfully.', 'transaction_hash': tx_hash}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
