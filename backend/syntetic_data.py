import numpy as np
import random
import time
import pandas as pd

# Membuat dataset sintetik
def generate_synthetic_data(num_records=5000):
    data = []
    for _ in range(num_records):
        voter_id = random.randint(1, 100)  # ID pemilih acak
        candidate_id = random.randint(101, 105)  # ID kandidat acak
        vote_time = int(time.time()) + random.randint(-3600, 3600)  # Waktu pemungutan suara acak sekitar waktu saat ini
        label = 0  # Default suara sah
        # Mensimulasikan suara ganda untuk pemilih yang sama dalam waktu singkat
        if random.random() < 0.05:  # 5% kesempatan untuk suara ganda
            label = 1
        data.append([voter_id, candidate_id, vote_time, label])
    return np.array(data)

# Generate dataset sintetik
synthetic_data = generate_synthetic_data(500)

# Mengonversi data ke DataFrame pandas
df = pd.DataFrame(synthetic_data, columns=["voter_id", "candidate_id", "vote_time", "label"])

# Menyimpan DataFrame ke file CSV
df.to_csv('dataset.csv', index=False)

# Menampilkan 10 data pertama
print(df.head())
