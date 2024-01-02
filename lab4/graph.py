import pandas as pd
import matplotlib.pyplot as plt

linear_df = pd.read_csv("data/linear.csv")
parallel_df = pd.read_csv("data/parallel.csv")

plt.plot(linear_df["N"], linear_df["Time"], label="Linear")
plt.plot(parallel_df["N"], parallel_df["Time"], label="Parallel")
plt.legend()
plt.xlabel("N")
plt.ylabel("Time")
plt.show()
