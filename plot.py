import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Sample data
y = [298.991, 202.346, 86.532, 62.826, 72.728, 32.730, 25.476, 25.239, 23.334, 21.281]
x = [10, 15, 20, 25, 30, 75, 80, 85, 90, 95]

# Define the type of function to fit
def exponential(x, a, b, c):
    return a * np.exp(-b * x) + c

# Fit the exponential function to the data
params, covariance = curve_fit(exponential, x, y, p0=[0, 0.01, 100])

# Generate x values for the curve (from min x to max x)
x_values = np.linspace(min(x), max(x), 400)

# Generate y values for the curve using the parameters obtained from curve fitting
y_values = exponential(x_values, *params)

plt.figure(figsize=(12, 5))  # Setting the figure size
plt.scatter(x, y, color='blue')  # Creating the scatter plot
plt.plot(x_values, y_values, color='red', label='Curva exponencial de mejor ajuste')  # Plotting the fitted curve

# Setting x-axis ticks every 5 units
plt.xticks(range(min(x), max(x) + 1, 5))

# Adding title and labels
plt.title('Tiempo de procesamiento en función del valor de swappiness para un espacio virtual de 4GB en un sistema con 0,5GB de memoria principal')
plt.xlabel('Swappiness')
plt.ylabel('Tiempo de procesamiento (s)')

# Optional: Add grid and legend
plt.grid(True)
plt.legend()

# Show the plot
plt.savefig('graph_with_curve.png')
