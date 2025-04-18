# --------- INTERACTIVE STRATEGY HELPER ---------

# Resets for interactive mode
color_counters = {"red": 0, "black": 0}

def update_counters(color_input):
    if color_input == "red":
        color_counters["red"] += 1
        color_counters["black"] = 0
    elif color_input == "black":
        color_counters["black"] += 1
        color_counters["red"] = 0
    else:
        color_counters["red"] = 0
        color_counters["black"] = 0

def get_bet_recommendation():
    if color_counters["red"] >= 3:
        bet_color = "black"
        bet_multiplier = 2 if color_counters["red"] > 3 else 1
        return f"Streak detected: {color_counters['red']}x RED → Bet on BLACK with {bet_multiplier}x base bet."
    elif color_counters["black"] >= 3:
        bet_color = "red"
        bet_multiplier = 2 if color_counters["black"] > 3 else 1
        return f"Streak detected: {color_counters['black']}x BLACK → Bet on RED with {bet_multiplier}x base bet."
    else:
        return "No streak yet. No bet recommended."

# --------- MAIN INTERACTION LOOP ---------

print("Roulette Strategy Advisor - Streak Counter")
print("Type 'red', 'black', or 'green' (for 0). Type 'exit' to quit.\n")

while True:
    color = input("Enter result color: ").strip().lower()
    
    if color == "exit":
        print("Exiting. Good luck!")
        break
    if color not in {"red", "black", "green"}:
        print("Invalid input. Please enter 'red', 'black', or 'green'.")
        continue

    update_counters(color)
    recommendation = get_bet_recommendation()
    print(recommendation)
    print(f"Current streaks → RED: {color_counters['red']}, BLACK: {color_counters['black']}\n")
