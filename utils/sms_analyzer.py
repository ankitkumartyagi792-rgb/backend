import re

def extract_suspicious_words(text):
    """Find suspicious words in text based on a predefined list."""
    suspicious_keywords = ["pay immediately", "disconnect", "urgent", "won", "prize", "jackpot", "claim", "restricted", "verify", "unpaid bill", "security alert", "unauthorized", "bank details"]
    text_lower = text.lower()
    found_words = []
    
    for word in suspicious_keywords:
        if word in text_lower:
            found_words.append(word)
            
    return found_words
