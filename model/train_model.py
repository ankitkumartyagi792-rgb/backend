import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import re

# Create directories if not exist
os.makedirs('model', exist_ok=True)
os.makedirs('dataset', exist_ok=True)

# 1. Create Dummy Dataset (In real scenario, load from a large CSV)
data = [
    # Fraud Messages
    ("URGENT! Your bank account is locked. Click http://fake-bank.com to verify.", 1),
    ("Congratulations! You've won a lottery of $5000. Claim now at http://win-prize.xyz.", 1),
    ("Your electricity will be disconnected tonight. Pay immediately at http://ele-bill.ml.", 1),
    ("KYC update required for your account. Visit http://kyc-fraud.tk to update.", 1),
    ("Your OTP is 4562. Do not share with anyone. Click to verify.", 1),
    ("Your PayPal account is limited. Restore access at http://secure-login.ga.", 1),
    ("Work from home and earn $500 daily. Register now!", 1),
    
    # Safe Messages
    ("Hey, are we still meeting for lunch tomorrow at 1 PM?", 0),
    ("Your appointment is confirmed for Monday at 3 PM.", 0),
    ("Thanks for your purchase! Your order has been shipped.", 0),
    ("Don't forget to bring the reports to the office.", 0),
    ("Happy Birthday! Wishing you a great year ahead.", 0),
    ("The meeting has been rescheduled to Friday.", 0),
    ("Can you please send me the photos from last night?", 0),
]

df = pd.DataFrame(data, columns=['message', 'label'])

# Save dataset
df.to_csv('dataset/fraud_sms_dataset.csv', index=False)

# 2. Preprocessing Function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text) # Remove special chars/numbers
    return text

df['clean_msg'] = df['message'].apply(clean_text)

# 3. Vectorization (TF-IDF)
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X = vectorizer.fit_transform(df['clean_msg'])
y = df['label']

# 4. Train Model
model = LogisticRegression()
model.fit(X, y)

# 5. Save Model and Vectorizer
with open('model/fraud_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Model trained and saved successfully!")
print("Files created: model/fraud_model.pkl, model/vectorizer.pkl")