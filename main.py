from flask import Flask, render_template, request
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from encecolormaps import palette

app = Flask(__name__, template_folder='templates', static_folder='static')

custom_palette = palette.palettes['20bnw']
csv_file_path = 'datasets/top250sorted.csv'

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

    if user_choice.lower() == 'heatmap':
        heatmap_data = selected_df.pivot(index='Season', columns='Episode', values='Rating')

        plt.figure(figsize=(16, 4))
        sns.heatmap(heatmap_data, cmap=custom_palette, annot=True, fmt=".1f", linewidths=.5)

        plt.title(f'{selected_show} Ratings Heatmap')
        img_path = 'static/heatmap.png'
        plt.savefig(img_path)
        plt.close()
        return render_template('result.html', img_path=img_path, selected_show=selected_show)
    elif user_choice.lower() == 'graph':
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='Episode', y='Rating', hue='Season', data=selected_df, marker='o', palette='viridis')

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
