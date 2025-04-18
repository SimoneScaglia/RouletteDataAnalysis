# --------- STRATEGIA UNIFICATA CON PUNTATA BASE ---------

# Configurazione iniziale
color_counters = {"rosso": 0, "nero": 0}
parity_counters = {"pari": 0, "dispari": 0}

# Tavola dei colori (roulette europea)
rosso_numeri = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
nero_numeri = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

def get_color(numero):
    if numero == 0:
        return "verde"
    elif numero in rosso_numeri:
        return "rosso"
    elif numero in nero_numeri:
        return "nero"
    else:
        return None

def get_parity(numero):
    if numero == 0:
        return "zero"
    return "pari" if numero % 2 == 0 else "dispari"

def aggiorna_color_counter(colore):
    if colore == "rosso":
        color_counters["rosso"] += 1
        color_counters["nero"] = 0
    elif colore == "nero":
        color_counters["nero"] += 1
        color_counters["rosso"] = 0
    else:
        color_counters["rosso"] = 0
        color_counters["nero"] = 0

def aggiorna_parity_counter(parity):
    if parity == "pari":
        parity_counters["pari"] += 1
        parity_counters["dispari"] = 0
    elif parity == "dispari":
        parity_counters["dispari"] += 1
        parity_counters["pari"] = 0
    else:
        parity_counters["pari"] = 0
        parity_counters["dispari"] = 0

def calcola_puntata_base(multiplicatore, puntata_base):
    return puntata_base * multiplicatore

# Funzione per calcolare il moltiplicatore (se il counter è > 3)
def calcola_moltiplicatore(counter):
    if counter > 3:
        return 2 * (counter - 3)  # Moltiplicatore = 2 * (counter - 3)
    return 1  # Altrimenti il moltiplicatore è 1

def raccomandazione_colore(puntata_base):
    if color_counters["rosso"] >= 3:
        moltiplicatore = calcola_moltiplicatore(color_counters["rosso"])
        puntata = calcola_puntata_base(moltiplicatore, puntata_base)
        return f"Streak rilevata: {color_counters['rosso']}x ROSSO → Punta su NERO con {puntata}€."
    elif color_counters["nero"] >= 3:
        moltiplicatore = calcola_moltiplicatore(color_counters["nero"])
        puntata = calcola_puntata_base(moltiplicatore, puntata_base)
        return f"Streak rilevata: {color_counters['nero']}x NERO → Punta su ROSSO con {puntata}€."
    else:
        return "Nessuna streak colore. Nessuna puntata consigliata."

def raccomandazione_parity(puntata_base):
    if parity_counters["pari"] >= 3:
        moltiplicatore = calcola_moltiplicatore(parity_counters["pari"])
        puntata = calcola_puntata_base(moltiplicatore, puntata_base)
        return f"Streak rilevata: {parity_counters['pari']}x PARI → Punta su DISPARI con {puntata}€."
    elif parity_counters["dispari"] >= 3:
        moltiplicatore = calcola_moltiplicatore(parity_counters["dispari"])
        puntata = calcola_puntata_base(moltiplicatore, puntata_base)
        return f"Streak rilevata: {parity_counters['dispari']}x DISPARI → Punta su PARI con {puntata}€."
    else:
        return "Nessuna streak parità. Nessuna puntata consigliata."

# --------- LOOP PRINCIPALE ---------

print("🧠 Consigliere Roulette - Analisi Colore & Parità")
print("Inserisci il numero uscito (0-36) e la puntata base (in euro). Digita 'exit' per uscire.\n")

puntata_base = float(input("Inserisci la tua puntata base (in euro): ").strip())

while True:
    inp = input("Numero uscito: ").strip().lower()
    if inp == "exit":
        print("Uscita dal programma. Buona fortuna!")
        break

    if not inp.isdigit():
        print("Input non valido. Inserisci un numero tra 0 e 36.\n")
        continue

    numero = int(inp)
    if numero < 0 or numero > 36:
        print("Numero fuori intervallo. Inserisci un numero tra 0 e 36.\n")
        continue

    colore = get_color(numero)
    parita = get_parity(numero)

    aggiorna_color_counter(colore)
    aggiorna_parity_counter(parita)

    print(f"→ Colore: {colore.upper()}, Parità: {parita.upper()}")
    print(raccomandazione_colore(puntata_base))
    print(raccomandazione_parity(puntata_base))
    print(f"Streak attuali → ROSSO: {color_counters['rosso']}, NERO: {color_counters['nero']} | PARI: {parity_counters['pari']}, DISPARI: {parity_counters['dispari']}\n")
