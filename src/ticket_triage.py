
import pandas as pd
import re
import json
import time
import random
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import mockllm
from mockllm import chat

BASE_DELAY = 0.05
MAX_RETRIES = 3

def call_with_retry(messages, ticket_id="TEST"):
    for n in range(MAX_RETRIES):
        try:
            response = chat(messages)
            return response
        except mockllm.TransientLLMError:
            wait = BASE_DELAY * (2 ** n) * random.uniform(0.9, 1.15)
            print(f"Retry ticket={ticket_id}, retry={n}, wait={wait:.4f}s")
            time.sleep(wait)

    raise RuntimeError(f"Ticket {ticket_id} failed after retries")

# Load tickets
tickets = pd.read_csv("data/processed/tickets_clean.csv")

ALLOWED_CATEGORIES = ["billing", "delivery", "technical", "fraud"]
MAX_INPUT_TOKENS = 400

def check_input(text):
    if pd.isna(text) or not str(text).strip():
        return "skipped_empty"

    estimated_tokens = len(str(text).split())

    if estimated_tokens > MAX_INPUT_TOKENS:
        return "flagged_long"

    return "eligible"

# Test input guardrails
print("INPUT GUARDRAIL TEST")
print("Empty:", check_input(""))
print("Long:", check_input("word " * 401))
print("Normal:", check_input("My order is delayed"))
# PII Redaction
def redact_pii(text):
    text = str(text)

    # Redact email addresses
    text = re.sub(
        r'\b[\w.-]+@[\w.-]+\.\w+\b',
        '[EMAIL]',
        text
    )

    # Redact Indian mobile numbers
    text = re.sub(
        r'\b(?:\+91[-\s]?)?[6-9]\d{9}\b',
        '[PHONE]',
        text
    )

    # Redact Aadhaar-like 12-digit numbers
    text = re.sub(
        r'\b\d{12}\b',
        '[ID]',
        text
    )

    return text


# Test PII redaction
sample = "Contact me at test@gmail.com or 9876543210"
print("Original:", sample)
print("Redacted:", redact_pii(sample))
# Zero-shot classification
def zero_shot_classify(text):
    prompt = f"""
CLASSIFY
Classify this support ticket into one category:
billing, delivery, technical, fraud.

Ticket: {redact_pii(text)}
"""
    response = call_with_retry([{"role": "system", "content": prompt}])
    return response.choices[0].message.content
print("\nZERO SHOT TEST")
print(zero_shot_classify("My payment was deducted twice"))

# Few-shot classification
def few_shot_classify(text):
    prompt = f"""
CLASSIFY
Classify this support ticket into one category:
billing, delivery, technical, fraud.

Return JSON only:
{{"category": "...", "reason": "..."}}

EXAMPLES:
Ticket: My payment was deducted twice
{{"category": "billing", "reason": "duplicate payment"}}

Ticket: My order has not arrived
{{"category": "delivery", "reason": "delayed order"}}

Ticket: Someone hacked my account
{{"category": "fraud", "reason": "account security"}}

Ticket: App keeps crashing
{{"category": "technical", "reason": "app issue"}}

Ticket: {redact_pii(text)}
"""
    response = chat([{"role": "system", "content": prompt}])
    return response.choices[0].message.content

print("\nFEW SHOT TEST")
print(few_shot_classify("My order has not arrived"))
print("\nRETRY TEST")
mockllm.reset()
