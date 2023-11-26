import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sszpalette

colormaps = sszpalette.register()

csv_file_path = 'datasets/00.imdb_top_250_series_episode_ratings.csv'

df = pd.read_csv(csv_file_path)

selected_show = input("Enter the name of the series: ")

selected_df = df[df['Title'] == selected_show]


user_choice = input("Select heatmap or graph: ")

if user_choice.lower() == 'heatmap':
    heatmap_data = selected_df.pivot(index='Season', columns='Episode', values='Rating')

    plt.figure(figsize=(18, 6))
    sns.heatmap(heatmap_data, cmap='autumn_r', annot=True, fmt=".1f", linewidths=.5)
    plt.title(f'{selected_show} Ratings Heatmap')
    plt.show()
elif user_choice.lower() == 'graph':
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Episode', y='Rating', hue='Season', data=selected_df, marker='o', palette='sequential9rot')

    plt.title(f'{selected_show} Ratings Graph')
    plt.xlabel('Episode')
    plt.ylabel('Rating')
    plt.legend(title='Season', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()
else:
    print("Invalid choice. Please enter 'heatmap' or 'graph'.")
