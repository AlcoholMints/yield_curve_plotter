import matplotlib.pyplot as plt
import numpy as np


headers = [0.08333333333333333, 0.16666666666666666, 0.25, 0.3333333333333333, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0]
data = [5.54, 5.51, 5.54, 5.52, 5.5, 5.33, 4.78, 4.45, 4.15, 4.1, 4.05, 4.36, 4.21]
date = 'fuck you'

def plot_yield_curve(headers, date, data):
    print(headers)
    print(data)
    print(date)
    print(plt.style.available[:])
    
    with plt.style.context('/Users/collin/Documents/GitHub/yield_curve_poster/rose-pine.mplstyle'):
        plt.figure(figsize=(6, 3.5))
        plt.plot(headers, data, marker = '.')
        plt.xlabel("Maturity (Years)")
        plt.ylabel("Yield")
        plt.title(f"US Treasury Yield Curve Rates on {date}")
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    plot_yield_curve(headers, date, data)