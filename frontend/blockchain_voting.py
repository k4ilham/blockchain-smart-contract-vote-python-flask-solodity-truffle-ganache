from web3 import Web3
import json
import requests

# Membaca konfigurasi dari file JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Koneksi ke Ganache
web3 = Web3(Web3.HTTPProvider(config["ganache_url"]))

# Alamat smart contract (dari hasil deploy Truffle)
contract_address = config["contract_address"]

# Simulate an admin account for demonstration purposes
admin_account = config["admin_account"]

# ABI dari smart contract
with open(config["contract_abi_path"], 'r') as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

# Inisialisasi kontrak
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Fungsi untuk mendapatkan status admin
def get_admin():
    return contract.functions.owner().call()

# Fungsi untuk mendeteksi apakah pemilih terdaftar
def is_voter_registered(voter_id):
    return contract.functions.voters(voter_id).call()[0]  # [0] untuk mendapatkan status isRegistered

# Fungsi untuk mendaftarkan pemilih
def register_voter(voter_id, admin_account):
    try:
        tx = contract.functions.registerVoter(voter_id).transact({'from': admin_account})
        web3.eth.wait_for_transaction_receipt(tx)
        return f"Voter {voter_id} has been successfully registered."
    except Exception as e:
        error_message = str(e)

        # Cari bagian 'reason' dari pesan error
        if "'reason': '" in error_message:
            start = error_message.find("'reason': '") + len("'reason': '")
            end = error_message.find("'", start)
            reason = error_message[start:end]
            reason = "Error registering voter: " + reason
        else:
            reason = "An unknown error occurred."

        return reason

# Fungsi untuk mendeteksi suara ganda (Double Vote)
def detect_double_vote(voter_id, candidate_id, vote_time):
    url = "http://127.0.0.1:5000/detect_double_vote"
    data = {
        'voter_id': voter_id,
        'candidate_id': candidate_id,
        'vote_time': vote_time
    }

    print("Sending request with data:", data)  # Debugging line
    try:
        # Pastikan kita mengirim data dengan format JSON dan menggunakan POST
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        # Memeriksa hasil response dan mengembalikan statusnya
        result = response.json()
        if 'status' in result:
            return result['status']
        else:
            print("Error: 'status' key not found in response.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error with ML server: {e}")
        return None

# Fungsi untuk memberikan suara
def cast_vote(voter_id, candidate_id, vote_time):
    try:
        candidate_id_int = int(candidate_id)  # Convert to integer

        # Periksa apakah pemilih sudah terdaftar
        if not is_voter_registered(voter_id):
            return f"Error casting vote: Voter {voter_id} is not registered!"

        # Deteksi suara ganda dengan ML Server
        vote_status = detect_double_vote(voter_id, candidate_id, vote_time)
        if vote_status == "Double Vote":
            return f"Error casting vote: Voter {voter_id} has already voted!"

        # Jika tidak ada suara ganda, lanjutkan untuk memberikan suara
        tx = contract.functions.castVote(candidate_id_int).transact({'from': voter_id})
        web3.eth.wait_for_transaction_receipt(tx)
        return f"Voter {voter_id} successfully cast vote for candidate {candidate_id} at {vote_time}"

    except Exception as e:
        error_message = str(e)

        # Cari bagian 'reason' dari pesan error
        if "'reason': '" in error_message:
            start = error_message.find("'reason': '") + len("'reason': '")
            end = error_message.find("'", start)
            reason = error_message[start:end]
            reason = "Error casting vote: " + reason
        else:
            reason = "An unknown error occurred."

        return reason

# Fungsi untuk mendapatkan hasil suara kandidat
def get_candidates_votes():
    candidates = contract.functions.getCandidates().call()
    results = []
    for candidate in candidates:
        candidate_id = candidate[0]
        candidate_name = candidate[1]
        votes = contract.functions.getCandidateVotes(candidate_id).call()
        results.append({
            'id': candidate_id,
            'name': candidate_name,
            'votes': votes
        })
    return results





