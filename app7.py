
from flask import Flask, render_template, request, jsonify
from networkx.drawing.layout import shell_layout
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
import ipywidgets as widgets
from IPython.display import display, HTML, Image
import colorsys
app7 = Flask(__name__)

# Load the dataset from a CSV file
dataset = pd.read_csv('TradePath.csv')

def find_all_paths(source, graph):
    all_paths = []
    for node in graph.nodes():
        if node != source:
            paths = list(nx.all_simple_paths(graph, source=source, target=node))
            if paths:
                all_paths.extend(paths)
    return all_paths


@app7.route('/')
def index():
    return render_template('app6_index.html')

@app7.route('/app6_index.html')
def app6_index():
    return render_template('app6_index.html')
# New route to handle AJAX requests for suggestions

# ...

# Route to fetch autocomplete suggestions
@app7.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    query = request.form.get('query')

    # Filter and retrieve matching suggestions from your dataset
    matching_suggestions = dataset['Source'].str.contains(query, case=False) | dataset['Target'].str.contains(query, case=False)

    suggestions = dataset.loc[matching_suggestions, 'Source'].tolist() + dataset.loc[matching_suggestions, 'Target'].tolist()

    # Deduplicate and return suggestions as JSON
    suggestions = list(set(suggestions))
    return jsonify(suggestions)

# ...
def make_brighter_color(color, brightness_factor=5):
    # Convert the color to the HSL color space
    r, g, b = [x / 255.0 for x in color]  # Convert RGB values to the range [0, 1]
    h, l, s = colorsys.rgb_to_hls(r, g, b)  # Convert to HSL

    # Increase the lightness (brightness) value
    l = min(1.0, l * brightness_factor)

    # Convert the modified HSL back to RGB
    r, g, b = colorsys.hls_to_rgb(h, l, s)

    # Convert RGB values back to the range [0, 255]
    r, g, b = [int(x * 255) for x in (r, g, b)]

    return (r, g, b)

# Example usage:
original_color = (255, 0, 0)  # Red color (RGB)
brighter_color = make_brighter_color(original_color)

print("Original Color:", original_color)
print("Brighter Color:", brighter_color)

@app7.route('/app6_search', methods=['POST'])
def app6_search():
    source = request.form['source']

    G = nx.Graph()
    G.add_edges_from(dataset[['Source', 'Target']].values)

    all_paths = find_all_paths(source, G)

    if all_paths:
        return jsonify({'paths': all_paths})

    return jsonify({'error_message': 'No paths found from the source'})

if __name__ == '__main__':
    app7.run(debug=True, port=50067)
