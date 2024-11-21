import requests

# URL server Flask
url = "http://127.0.0.1:5000/detect_double_vote"

# Data suara (contoh untuk pemilih dengan voter_id = 1)
vote_data = {
    "voter_id": 1,
    "candidate_id": 101,
    "vote_time": 1637846400  # Timestamp
}

# Kirimkan permintaan POST ke server Flask
response = requests.post(url, json=vote_data)

# Tampilkan respon dari server
print("Response:", response.json())

# Tes Double Vote
double_vote_data = {
    "voter_id": 1,
    "candidate_id": 101,
    "vote_time": 1637846410  # Timestamp berbeda untuk pengujian double vote
}
response = requests.post(url, json=double_vote_data)
print("Response (Double Vote):", response.json())
