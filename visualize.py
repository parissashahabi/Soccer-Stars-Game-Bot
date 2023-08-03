import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


def avg_fitness():
    csv_file_path = 'simulation/history.csv'

    data = pd.read_csv(csv_file_path)
    data = data.values.flatten()

    N_ITER = len(data)

    sb.set_style("darkgrid")
    plt.figure(figsize=(8, 6))

    # Plot the data from the CSV file
    sb.lineplot(x=range(1, N_ITER + 1), y=data)

    # Add labels and legend
    plt.ylabel('Fitness')
    plt.xlabel('Generation')

    # Show the plot
    plt.show()


if __name__ == '__main__':
    avg_fitness()
