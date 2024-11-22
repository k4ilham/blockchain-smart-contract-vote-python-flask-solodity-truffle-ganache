import requests
from web3 import Web3
import json
import time

# Koneksi ke Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Pastikan koneksi berhasil
if web3.is_connected():
    print("Connected to Ganache!")

# Alamat smart contract (dari hasil deploy Truffle)
contract_address = "0x633d11283CC66C9ea9BCE52D6D6A41CD435DaED0"

# ABI dari smart contract
with open('../smart_contracts/build/contracts/BlockchainVoting.json', 'r') as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

# Inisialisasi kontrak
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Alamat admin dari Ganache
admin_account = web3.eth.accounts[0]

# Fungsi untuk mendeteksi suara ganda ke ML server
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

# Fungsi untuk memeriksa apakah pemilih terdaftar
def is_voter_registered(voter_id):
    # Periksa status isRegistered dari mapping voters
    return contract.functions.voters(voter_id).call()[0]  # [0] untuk mendapatkan status isRegistered

# Fungsi untuk mendaftarkan pemilih
def register_voter(voter_id):
    try:
        # Mendaftarkan pemilih dari akun admin
        tx = contract.functions.registerVoter(voter_id).transact({'from': admin_account})
        web3.eth.wait_for_transaction_receipt(tx)
        print(f"Voter {voter_id} has been successfully registered.")
    except Exception as e:
        print(f"Error registering voter: {e}")

# Fungsi untuk memberikan suara
def cast_vote(voter_id, candidate_id):
    # Mendapatkan timestamp saat ini
    vote_time = int(time.time())  # Waktu saat ini dalam format Unix timestamp

    # Periksa apakah pemilih sudah terdaftar
    if not is_voter_registered(voter_id):
        print(f"Voter {voter_id} is not registered! Registering now...")
        register_voter(voter_id)  # Mendaftarkan pemilih jika belum terdaftar
        return

    # Deteksi suara ganda dengan ML Server
    vote_status = detect_double_vote(voter_id, candidate_id, vote_time)
    
    if vote_status == "Double Vote":
        print(f"Voter {voter_id} has already voted!")
        return

    # Jika tidak ada suara ganda, lanjutkan untuk memberikan suara
    try:
        tx = contract.functions.castVote(candidate_id).transact({'from': voter_id})
        web3.eth.wait_for_transaction_receipt(tx)
        print(f"Voter {voter_id} cast vote for candidate {candidate_id} at {vote_time}")
    except Exception as e:
        print(f"Error casting vote: {e}")

# Fungsi untuk menampilkan jumlah suara untuk masing-masing kandidat
def display_candidate_votes():
    print("\nVotes for each candidate:")
    
    # Mendapatkan semua kandidat dari kontrak
    candidates = contract.functions.getCandidates().call()

    # Menampilkan kandidat dan jumlah suara mereka
    for candidate in candidates:
        candidate_id = candidate[0]
        candidate_name = candidate[1]
        candidate_votes = contract.functions.getCandidateVotes(candidate_id).call()
        
        print(f"Candidate {candidate_name} (ID: {candidate_id}) has {candidate_votes} votes.")

# Contoh penggunaan
if __name__ == "__main__":

    voter1 = web3.eth.accounts[7]
    voter2 = web3.eth.accounts[8]
    
    # Pemilih pertama memberi suara dengan waktu otomatis
    cast_vote(voter1, 2)
    # Delay 1 detik untuk memastikan waktu berbeda antara pemilih
    time.sleep(1)
    # Pemilih kedua memberi suara dengan waktu otomatis
    cast_vote(voter2, 2)

    # Menampilkan jumlah suara untuk setiap kandidat
    display_candidate_votes()
