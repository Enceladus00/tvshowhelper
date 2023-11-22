import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

csv_file_path = 'datasets/00.imdb_top_250_series_episode_ratings.csv'

df = pd.read_csv(csv_file_path)

selected_show = 'Narcos'

selected_df = df[df['Title'] == selected_show]

heatmap_data = selected_df.pivot(index='Season', columns='Episode', values='Rating')

plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='viridis', annot=True, fmt=".1f", linewidths=.5)
plt.title(f'{selected_show} Ratings Heatmap')
plt.show()
