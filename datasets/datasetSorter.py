import pandas as pd

# Load the CSV file
df = pd.read_csv("imdbTop250.csv")

# Sort by the 'Title' column
df_sorted = df.sort_values(by="Title")

# Save the sorted data to a new CSV file
df_sorted.to_csv("imdbTop250Sorted.csv", index=False)

print("Sorting complete. Saved as sorted_file.csv")
