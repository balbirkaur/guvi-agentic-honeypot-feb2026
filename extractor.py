import re

def extract(text, store):
    store["upiIds"] += re.findall(r'[\w.-]+@[\w]+', text)
    store["phishingLinks"] += re.findall(r'https?://[^\s]+', text)
    store["bankAccounts"] += re.findall(r'\b\d{9,18}\b', text)
    store["phoneNumbers"] += re.findall(r'\+91\d{10}', text)
