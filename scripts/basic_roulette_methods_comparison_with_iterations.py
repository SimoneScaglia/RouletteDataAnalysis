import random
import matplotlib.pyplot as plt
import pandas as pd
import os

results_dir = "../results"
os.makedirs(results_dir, exist_ok=True)

# Impostazioni iniziali
saldo_iniziale = 5000
saldo_esci = 6000
giocate = 500
puntata_base = 10
n_iterazioni = 5000

# Numeri per colore
numeri_neri = {
    2, 4, 6, 8, 10, 11, 13, 15, 17, 20,
    22, 24, 26, 28, 29, 31, 33, 35
}
numeri_rossi = {
    1, 3, 5, 7, 9, 12, 14, 16, 18, 19,
    21, 23, 25, 27, 30, 32, 34, 36
}

# --------- STRATEGIE ---------
def martingala(numero, puntata, saldo, stato):
    return {"tipo": "nero", "raddoppia": True, "resetta": True}

def dalembert(numero, puntata, saldo, stato):
    if "livello" not in stato:
        stato["livello"] = 1
    scelta = {"tipo": "rosso"}

    if stato.get("esito_precedente") is not None:
        if stato["esito_precedente"]:
            stato["livello"] = max(1, stato["livello"] - 1)
        else:
            stato["livello"] += 1

    scelta["puntata"] = puntata_base * stato["livello"]
    stato["puntata_corrente"] = scelta["puntata"]
    return scelta

def puntate_ibride(numero, puntata, saldo, stato):
    tipi = ["rosso", "nero", "pari", "dispari"]
    return {"tipo": random.choice(tipi)}

def oscars_grind(numero, puntata, saldo, stato):
    if "profitto_sessione" not in stato:
        stato["profitto_sessione"] = 0
        stato["puntata_corrente"] = puntata_base

    scelta = {"tipo": "rosso", "puntata": stato["puntata_corrente"]}
    return scelta

# --------- SIMULAZIONE ---------
def simula(strategy_func):
    saldo = saldo_iniziale
    storico = []
    stato = {}
    i = 0
    puntata = puntata_base

    while i < giocate and saldo >= puntata_base:
        if saldo >= saldo_esci:
            break

        numero = random.randint(0, 36)
        scelta = strategy_func(numero, puntata, saldo, stato)

        # Puntata personalizzata se fornita
        puntata = scelta.get("puntata", puntata_base)
        puntata = min(puntata, saldo)

        if scelta["tipo"] == "nero":
            vincita = numero in numeri_neri
        elif scelta["tipo"] == "rosso":
            vincita = numero in numeri_rossi
        elif scelta["tipo"] == "pari":
            vincita = numero != 0 and numero % 2 == 0
        elif scelta["tipo"] == "dispari":
            vincita = numero % 2 == 1
        elif scelta["tipo"] == "numero":
            vincita = numero == scelta["valore"]
        else:
            vincita = False

        if vincita:
            saldo += puntata
            if scelta.get("raddoppia"):
                pass
            if scelta.get("resetta"):
                puntata = puntata_base
            if strategy_func == oscars_grind:
                stato["profitto_sessione"] += puntata
                if stato["profitto_sessione"] >= puntata_base:
                    stato["profitto_sessione"] = 0
                    stato["puntata_corrente"] = puntata_base
                else:
                    stato["puntata_corrente"] = min(saldo, stato["puntata_corrente"] + puntata_base)
        else:
            saldo -= puntata
            if scelta.get("raddoppia"):
                puntata *= 2
            elif scelta.get("resetta"):
                puntata = puntata_base
            if strategy_func == oscars_grind:
                stato["puntata_corrente"] = puntata_base

        stato["esito_precedente"] = vincita
        storico.append(saldo)
        i += 1

    return storico

# --------- METRICHE ---------
def calcola_metriche(nome, storico):
    saldo_finale = storico[-1]
    guadagno = saldo_finale - saldo_iniziale
    guadagno_perc = (guadagno / saldo_iniziale) * 100
    durata = len(storico)

    max_drawdown = 0
    picco = storico[0]
    for s in storico:
        if s > picco:
            picco = s
        drawdown = picco - s
        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return {
        "Strategia": nome,
        "Durata (giocate)": durata,
        "Saldo finale (€)": saldo_finale,
        "Guadagno (€)": guadagno,
        "Guadagno %": guadagno_perc,
        "Max Drawdown (€)": max_drawdown
    }

# --------- STRATEGIE DA TESTARE ---------
strategie = {
    "Martingala": martingala,
    "D'Alembert": dalembert,
    "Puntate Ibride": puntate_ibride,
    "Oscar's Grind": oscars_grind
}

# --------- ESECUZIONI MULTIPLE ---------
tutte_le_metriche = []

for nome, func in strategie.items():
    metriche_per_strategia = []
    for _ in range(n_iterazioni):
        storico = simula(func)
        m = calcola_metriche(nome, storico)
        metriche_per_strategia.append(m)

    # Calcolo medie
    df_tmp = pd.DataFrame(metriche_per_strategia)
    media_metriche = df_tmp.mean(numeric_only=True)
    media_metriche["Strategia"] = nome
    tutte_le_metriche.append(media_metriche)

# --------- TABELLA MEDIA ---------
df_medie = pd.DataFrame(tutte_le_metriche)
df_medie = df_medie[
    ["Strategia", "Durata (giocate)", "Saldo finale (€)", "Guadagno (€)", "Guadagno %", "Max Drawdown (€)"]
]
df_medie = df_medie.sort_values(by="Guadagno (€)", ascending=False)

# --------- SALVA TABELLA PNG ---------
fig, ax = plt.subplots(figsize=(12, len(df_medie) * 0.6 + 1))
ax.axis('off')
tabella = ax.table(cellText=df_medie.round(2).values,
                   colLabels=df_medie.columns,
                   cellLoc='center',
                   loc='center')
tabella.auto_set_font_size(False)
tabella.set_fontsize(10)
tabella.scale(1, 1.5)

plt.tight_layout()
plt.savefig(os.path.join(results_dir, "metriche_strategie_medie.png"), bbox_inches='tight')
plt.close()
