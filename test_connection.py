"""
Test rapid — Verifică dacă API-ul Claude funcționează
=====================================================
Rulează ÎNAINTE de chatbot.py ca să te asiguri că totul e OK.

    python test_connection.py
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# Verifică dacă API key-ul există
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key or api_key.startswith("sk-ant-api03-XXXX"):
    print("❌ API key lipsește sau e cel default!")
    print()
    print("Ce trebuie să faci:")
    print("  1. Du-te la https://console.anthropic.com/")
    print("  2. Creează un cont (sau loghează-te)")
    print("  3. Settings → API Keys → Create Key")
    print("  4. Copiază key-ul în fișierul .env:")
    print('     ANTHROPIC_API_KEY=sk-ant-api03-cheia-ta-aici')
    print()
    print("📌 Fișierul .env trebuie să fie în folderul marina-ai-chatbot/")
    exit(1)

print("✅ API key găsit!")
print(f"   Primele caractere: {api_key[:20]}...")
print()

# Trimite un mesaj simplu de test
print("📡 Trimit mesaj de test la Claude...")
print()

try:
    client = anthropic.Anthropic()
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": "Spune 'Salut! Conexiunea funcționează! 🎉' și nimic altceva."
        }]
    )
    
    print(f"🤖 Claude: {response.content[0].text}")
    print()
    print("=" * 45)
    print("  ✅ TOTUL FUNCȚIONEAZĂ!")
    print("  Acum poți rula: python chatbot.py")
    print("=" * 45)
    
except anthropic.AuthenticationError:
    print("❌ API key-ul e invalid! Verifică din nou.")
except Exception as e:
    print(f"❌ Eroare: {e}")
