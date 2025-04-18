import random
import matplotlib.pyplot as plt
import os

# --------- CONFIGURATION ---------
RESULTS_DIR = "../results"
os.makedirs(RESULTS_DIR, exist_ok=True)

INITIAL_BALANCE = 10
TARGET_BALANCE = 20
MAX_ROUNDS = 500
BASE_BET = 0.5

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

# --------- EXECUTION ---------
strategies = {"Streak Counter Strategy": streak_counter_strategy}
results = {name: simulate(func) for name, func in strategies.items()}

# --------- PLOT ---------
def generate_plot(results):
    fig, ax = plt.subplots()
    fig.suptitle("Roulette Simulation - Streak Counter Strategy", fontsize=18)

    for name, history in results.items():
        ax.plot(range(1, len(history) + 1), history, label=name)
    
    ax.axhline(y=INITIAL_BALANCE, color='gray', linestyle='--', label='Initial Balance')
    ax.set_xlabel("Round")
    ax.set_ylabel("Balance (€)")
    ax.grid(True)
    ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "streak_counter_strategy.png"))
    plt.close()

generate_plot(results)

# --------- PRINT METRICS ---------
for name, history in results.items():
    metrics = calculate_metrics(name, history)
