
# Roulette Strategy Simulation

This project simulates and compares four different roulette betting strategies over multiple iterations. The strategies tested are:

1. **Martingale**
2. **D'Alembert**
3. **Puntate Ibride**
4. **Oscar's Grind**

The simulation includes tracking key metrics like:
- Final balance
- Profit/loss in EUR
- Gain percentage
- Maximum drawdown

The goal is to evaluate the performance of each strategy over a large number of iterations and compare their effectiveness.

## Files in the Project

1. **basic_roulette_methods_comparison.py**
   - This script simulates the roulette game using four different strategies and generates results for one iteration.
   - The results are plotted and saved as images.
   - The key metrics (final balance, profit, drawdown, etc.) are saved to a CSV file and a PNG image.

2. **basic_roulette_methods_comparison_with_iterations.py**
   - This script extends the previous simulation by running multiple iterations (n iterations) for each strategy.
   - It calculates the average metrics for each strategy across all iterations and outputs the results to a CSV file and a PNG image.
   
### Requirements

To run the project, you need the following Python libraries:

- `matplotlib`
- `pandas`

You can install them via pip:

```bash
pip install matplotlib pandas
```

### Running the Scripts

1. **To run a single iteration with one strategy comparison:**

```bash
python basic_roulette_methods_comparison.py
```

2. **To run multiple iterations and calculate the average results for each strategy:**

```bash
python basic_roulette_methods_comparison_with_iterations.py
```

After execution, the following files will be generated:

- `strategie_roulette_completo.png` - A plot showing the progress of each strategy.
- `metriche_strategie.csv` - A CSV file containing the performance metrics for each strategy.
- `metriche_strategie.png` - A PNG image of the performance metrics table.
- `metriche_strategie_medie.png` - A PNG image of the average performance metrics for each strategy across all iterations.
  
The table will include the following metrics for each strategy:

- **Durata (giocate)**: The total number of games played.
- **Saldo finale (€)**: The final balance after the specified number of games.
- **Guadagno (€)**: The profit or loss compared to the initial balance.
- **Guadagno %**: The percentage of gain or loss compared to the initial balance.
- **Max Drawdown (€)**: The maximum loss from the highest balance during the game.

### Example Output

After running `basic_roulette_methods_comparison_with_iterations.py`, you should see a table like this in the output image `metriche_strategie_medie.png`:

| Strategia      | Durata (giocate) | Saldo finale (€) | Guadagno (€) | Guadagno % | Max Drawdown (€) |
|----------------|------------------|------------------|--------------|------------|------------------|
| Martingala     | 500              | 5200             | 200          | 4%         | 150              |
| D'Alembert     | 500              | 5100             | 100          | 2%         | 200              |
| Puntate Ibride | 500              | 5300             | 300          | 6%         | 100              |
| Oscar's Grind  | 500              | 5000             | 0            | 0%         | 250              |
