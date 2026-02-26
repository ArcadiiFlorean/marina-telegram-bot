"""
Marina AI Chatbot — Prima interacțiune cu Claude API
=====================================================
Acest script este PRIMUL pas în construirea chatbot-ului.
Rulează în terminal și simulează o conversație cu o mamă.

Cum rulezi:
    python chatbot.py

Ce învățăm aici:
    1. Cum funcționează biblioteca `anthropic`
    2. Ce e un "system prompt" și de ce e important
    3. Cum funcționează o conversație cu "memorie" (conversation history)
    4. Structura mesajelor: role (user/assistant) + content
"""

# ============================================
# IMPORTURI
# ============================================
# anthropic — biblioteca oficială pentru Claude API
# os — pentru a citi variabile din .env
# dotenv — încarcă automat fișierul .env
import anthropic
import os
from dotenv import load_dotenv

# Încarcă variabilele din fișierul .env (unde avem API key-ul)
load_dotenv()


# ============================================
# SYSTEM PROMPT — "Personalitatea" chatbot-ului
# ============================================
# Aceasta e INIMA chatbot-ului. Aici definim:
# - Cine este (asistent pe site-ul dr. Marina)
# - Ce știe (serviciile, prețurile)
# - Cum vorbește (cald, empatic, în română)
# - Ce NU face (nu dă sfaturi medicale directe)
#
# Un system prompt bun = un chatbot bun.
# Acesta va fi îmbunătățit în Săptămâna 3 cu RAG.

SYSTEM_PROMPT = """Ești asistentul virtual de pe site-ul dr. Marina Cociug — medic pediatru și consultant IBCLC certificat în alăptare.

MISIUNEA TA:
Ajuți mamele să găsească informațiile de care au nevoie și le ghidezi spre serviciul potrivit.

SERVICIILE DR. MARINA (consultații online, £39 fiecare):

1. 🤱 Consultație Alăptare
   - Pentru: mame care au dificultăți cu alăptarea, dureri, producție scăzută, poziții
   - Include: evaluare completă + plan personalizat
   - Potrivit pentru: sarcină tardivă sau după naștere

2. 🥣 Consultație Diversificare
   - Pentru: mame cu bebeluși de ~6 luni, gata de primele alimente solide
   - Include: plan alimentar pe etape, rețete, sfaturi practice
   - Recomandat de la 6 luni

3. 🌙 Consultație Înțărcare
   - Pentru: mame care vor să încheie alăptarea natural și fără stres
   - Include: plan gradual personalizat, suport emoțional
   - La orice vârstă a copilului

4. 💬 Comunitate Telegram
   - Grup privat de suport pentru mame
   - Acces la informații, discuții, și suportul dr. Marina

REGULILE TALE:
- Vorbești în ROMÂNĂ, cald și empatic, ca o prietenă care înțelege
- NU dai sfaturi medicale specifice — ghidezi mereu spre consultație
- Când mama exprimă o problemă concretă, sugerezi serviciul potrivit
- Când mama vrea să se programeze, o direcționezi spre pagina de programare
- Răspunsuri scurte și clare, nu eseuri — mamele sunt ocupate!
- Folosești ocazional emoji-uri relevante, dar nu exagerat
- Sloganul nostru: "Mame citite = mame liniștite" 📚

EXEMPLE DE REDIRECȚIONARE:
- "Vreau să mă programez" → "Poți face programarea aici: marina-cociug.com/programare 📅"
- "Cât costă?" → "Fiecare consultație este £39 și include evaluare completă + plan personalizat."
- "Bebelușul nu vrea să sugă" → Exprimă empatie, apoi sugerează Consultația de Alăptare

IMPORTANT:
Nu inventa informații medicale. Dacă nu știi ceva, spune sincer că dr. Marina poate oferi răspunsul în cadrul unei consultații personalizate."""


# ============================================
# INIȚIALIZARE CLIENT CLAUDE
# ============================================
# Clientul folosește automat ANTHROPIC_API_KEY din .env
client = anthropic.Anthropic()

# Lista de mesaje — aici se păstrează "memoria" conversației
# Fiecare mesaj are: {"role": "user"/"assistant", "content": "text"}
conversation_history = []


def chat(user_message: str) -> str:
    """
    Trimite un mesaj către Claude și primește răspunsul.
    
    Cum funcționează:
    1. Adaugă mesajul mamei în istoric
    2. Trimite TOTUL (system prompt + istoric) la Claude
    3. Claude vede toată conversația și răspunde în context
    4. Salvează răspunsul în istoric pentru următoarea rundă
    
    Args:
        user_message: Ce a scris mama în chat
    
    Returns:
        Răspunsul chatbot-ului
    """
    # Pas 1: Adaugă mesajul utilizatorului în istoric
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Pas 2: Trimite cererea la Claude API
    response = client.messages.create(
        model="claude-sonnet-4-20250514",  # Modelul Claude — bun și accesibil
        max_tokens=500,                     # Limită de răspuns (mamele vor răspunsuri scurte)
        system=SYSTEM_PROMPT,               # Personalitatea chatbot-ului
        messages=conversation_history       # Toată conversația până acum
    )
    
    # Pas 3: Extrage textul din răspuns
    # response.content e o listă de blocuri; noi luăm textul din primul bloc
    assistant_message = response.content[0].text
    
    # Pas 4: Salvează răspunsul în istoric (Claude va "ține minte" ce a zis)
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message


# ============================================
# BUCLA PRINCIPALĂ — Chat în terminal
# ============================================
def main():
    """
    Bucla de chat interactiv.
    Scrii un mesaj, primești răspuns. Scrii 'exit' ca să ieși.
    """
    print("=" * 55)
    print("  🤱 Marina AI Chatbot — Versiunea Terminal")
    print("  Site: marina-cociug.com")
    print("  Scrie 'exit' pentru a închide")
    print("=" * 55)
    print()
    
    while True:
        # Citește input de la utilizator
        user_input = input("👩 Mama: ").strip()
        
        # Verifică dacă vrea să iasă
        if user_input.lower() in ("exit", "quit", "q"):
            print("\n🤱 Chatbot: La revedere! Mame citite = mame liniștite! 📚\n")
            break
        
        # Nu trimite mesaje goale
        if not user_input:
            continue
        
        # Trimite mesajul și afișează răspunsul
        try:
            response = chat(user_input)
            print(f"\n🤱 Chatbot: {response}\n")
        except anthropic.AuthenticationError:
            print("\n❌ API key invalid! Verifică fișierul .env\n")
            print("   Pași:")
            print("   1. Du-te la https://console.anthropic.com/")
            print("   2. Creează un API key")
            print("   3. Copiază-l în fișierul .env")
            break
        except anthropic.RateLimitError:
            print("\n⏳ Prea multe cereri. Așteaptă câteva secunde și încearcă din nou.\n")
        except Exception as e:
            print(f"\n❌ Eroare: {e}\n")


# Punctul de start — Python rulează main() când lansezi scriptul
if __name__ == "__main__":
    main()
