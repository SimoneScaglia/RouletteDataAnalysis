import random
import matplotlib.pyplot as plt
import os
import pandas as pd

# --------- CONFIGURATION ---------
RESULTS_DIR = "../results"
os.makedirs(RESULTS_DIR, exist_ok=True)

INITIAL_BALANCE = 10
TARGET_BALANCE = 20
MAX_ROUNDS = 500
BASE_BET = 0.5
N_ITERATIONS = 5000

BLACK_NUMBERS = {
    2, 4, 6, 8, 10, 11, 13, 15, 17, 20,
    22, 24, 26, 28, 29, 31, 33, 35
}
RED_NUMBERS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18, 19,
    21, 23, 25, 27, 30, 32, 34, 36
}

# --------- STRATEGIES ---------
color_counters = {"red": 0, "black": 0}

def streak_counter_strategy(number, bet, balance, state):
    """Strategy that bets on the opposite color after 3 consecutive results."""
    if number in RED_NUMBERS:
        color_counters["red"] += 1
        color_counters["black"] = 0
    elif number in BLACK_NUMBERS:
        color_counters["black"] += 1
        color_counters["red"] = 0
    else:
        color_counters["red"] = 0
        color_counters["black"] = 0

    if color_counters["red"] >= 3:
        return {"type": "black", "bet": bet * (2 if color_counters["red"] > 3 else 1)}
    elif color_counters["black"] >= 3:
        return {"type": "red", "bet": bet * (2 if color_counters["black"] > 3 else 1)}
    else:
        return {"type": "none"}

# --------- SIMULATION ---------
def simulate(strategy_func):
    balance = INITIAL_BALANCE
    balance_history = []
    state = {}
    bet = BASE_BET
    number = 0

    for _ in range(MAX_ROUNDS):
        if balance >= TARGET_BALANCE or balance < BASE_BET:
            break

        decision = strategy_func(number, bet, balance, state)
        number = random.randint(0, 36)
        bet = min(decision.get("bet", BASE_BET), balance)

        if decision["type"] == "none":
            balance_history.append(balance)
            continue

        win = (
            (decision["type"] == "red" and number in RED_NUMBERS) or
            (decision["type"] == "black" and number in BLACK_NUMBERS)
        )

        balance += bet if win else -bet
        state["previous_result"] = win
        balance_history.append(balance)

    return balance_history

# --------- METRICS ---------
def calculate_metrics(name, history):
    final_balance = history[-1]
    profit = final_balance - INITIAL_BALANCE
    profit_perc = (profit / INITIAL_BALANCE) * 100
    duration = len(history)

    max_drawdown = 0
    peak = history[0]
    for bal in history:
        peak = max(peak, bal)
        drawdown = peak - bal
        max_drawdown = max(max_drawdown, drawdown)

    return {
        "Strategy": name,
        "Duration (rounds)": duration,
        "Final Balance (€)": final_balance,
        "Profit (€)": profit,
        "Profit %": round(profit_perc, 2),
        "Max Drawdown (€)": max_drawdown
    }

strategies = {"Streak Counter Strategy": streak_counter_strategy}

# --------- ESECUZIONI MULTIPLE ---------
tutte_le_metriche = []

for nome, func in strategies.items():
    metriche_per_strategia = []
    for _ in range(N_ITERATIONS):
        storico = simulate(func)
        m = calculate_metrics(nome, storico)
        metriche_per_strategia.append(m)

    # Calcolo medie
    df_tmp = pd.DataFrame(metriche_per_strategia)
    media_metriche = df_tmp.mean(numeric_only=True)
    media_metriche["Strategy"] = nome
    tutte_le_metriche.append(media_metriche)

# --------- TABELLA MEDIA ---------
df_medie = pd.DataFrame(tutte_le_metriche)
df_medie = df_medie[
    ["Strategy", "Duration (rounds)", "Final Balance (€)", "Profit (€)", "Profit %", "Max Drawdown (€)"]
]
df_medie = df_medie.sort_values(by="Final Balance (€)", ascending=False)

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
plt.savefig(os.path.join(RESULTS_DIR, "streak_counter_method_mean.png"), bbox_inches='tight')
plt.close()
