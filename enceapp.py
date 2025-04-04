from flask import Flask, render_template, request
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from encecolormaps import palette
import imdb

ia = imdb.Cinemagoer()

app = Flask(__name__, template_folder='templates', static_folder='static')

custom_palette = palette.palettes['redngreen']
csv_file_path = 'datasets/imdbTop250Sorted.csv'

df = pd.read_csv(csv_file_path)
series_list = df['Title'].unique().tolist()


@app.route('/')
def index():
    return render_template('index.html', series_list=series_list)


@app.route('/result', methods=['POST'])
def result():
    selected_show = request.form['selected_show']
    user_choice = request.form['user_choice']

    selected_df = df[df['Title'] == selected_show]

    movies = ia.search_movie(selected_show)
    selected_series = movies[0]
    id = selected_series.movieID

    if user_choice.lower() == 'heatmap':
        heatmap_data = selected_df.pivot(index='Season', columns='Episode', values='Rating')

        plt.figure(figsize=(16, 4))
        ax = sns.heatmap(heatmap_data, cmap=custom_palette, annot=True, fmt=".1f", linewidths=.5)
        ax.set_facecolor('#ECE4D7')
        img_path = 'static/heatmap.png'
        plt.savefig(img_path)
        plt.close()
        highest_rated_episode = selected_df[selected_df['Rating'] == selected_df['Rating'].max()]['Episode'].iloc[0]
        lowest_rated_episode = selected_df[selected_df['Rating'] == selected_df['Rating'].min()]['Episode'].iloc[0]
        highest_rated_episode_season = selected_df[selected_df['Rating'] == selected_df['Rating'].max()]['Season'].iloc[
            0]
        lowest_rated_episode_season = selected_df[selected_df['Rating'] == selected_df['Rating'].min()]['Season'].iloc[
            0]
        return render_template('result.html', img_path=img_path, selected_show=selected_show,
                               highest_rated_episode=highest_rated_episode, lowest_rated_episode=lowest_rated_episode,
                               highest_rated_episode_season=highest_rated_episode_season,
                               lowest_rated_episode_season=lowest_rated_episode_season, id=id)
    elif user_choice.lower() == 'graph':
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='Episode', y='Rating', hue='Season', data=selected_df, marker='o', palette='inferno_r')

        plt.title(f'{selected_show} Ratings Graph')
        plt.xlabel('Episode')
        plt.ylabel('Rating')
        plt.legend(title='Season', bbox_to_anchor=(1.05, 1), loc='upper left')
        img_path = 'static/graph.png'
        plt.savefig(img_path)
        plt.close()
        return render_template('result.html', img_path=img_path)
    else:
        return "Invalid choice. Please enter 'heatmap' or 'graph'."


if __name__ == '__main__':
    app.run(debug=True)
