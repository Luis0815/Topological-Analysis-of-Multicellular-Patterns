#!/usr/bin/env python3

import os
import sys
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def clean_filename(filename):
    filename = os.path.splitext(filename)[0]
    return filename

def extract_levels(filename):
    parts = filename.split('_')
    for part in parts:
        if part.isdigit():
            return int(part)
    return 0

def sort_filenames(filenames):
    return sorted(filenames, key=extract_levels)

def reorder_matrix(matrix, filenames):
    sorted_filenames = sort_filenames(filenames)
    indices = [filenames.index(name) for name in sorted_filenames]
    reordered_matrix = matrix[np.ix_(indices, indices)]
    return reordered_matrix, sorted_filenames

def get_category(filename):
    base_name = filename.split('_')[0]
    if base_name == 'stroma':
        if 'carcinoma' in filename:
            return 'stroma_ad_carcinoma'
        elif 'dysplasia' in filename:
            return 'stroma_ad_dysplasia'
    elif base_name == 'carcinoma':
        return 'carcinoma'
    elif base_name == 'dysplasia':
        return 'dysplasia'
    return 'other'

def plot_heatmap_and_clustermap(matrix, filenames, title, output_dir):
    cleaned_filenames = [clean_filename(f) for f in filenames]
    reordered_matrix, sorted_filenames = reorder_matrix(matrix, cleaned_filenames)

    category_colors = {
        'carcinoma': '#E69F00',
        'dysplasia': '#9400D3',
        'stroma_ad_carcinoma': '#56B4E9',
        'stroma_ad_dysplasia': '#F9E79F',
        'other': '#999999'
    }

    # HEATMAP
    plt.figure(figsize=(12, 10))
    ax = sns.heatmap(reordered_matrix, xticklabels=sorted_filenames, yticklabels=sorted_filenames, cmap='viridis', annot=False)
    
    for label in ax.get_xticklabels():
        categoria = get_category(label.get_text())
        label.set_fontsize(6)
        label.set_color('black')
        label.set_bbox(dict(facecolor=category_colors[categoria], edgecolor='none', boxstyle='round,pad=0.2'))

    for label in ax.get_yticklabels():
        categoria = get_category(label.get_text())
        label.set_fontsize(6)
        label.set_color('black')
        label.set_bbox(dict(facecolor=category_colors[categoria], edgecolor='none', boxstyle='round,pad=0.2'))

    plt.title(f"Heatmap de {title}")
    plt.savefig(os.path.join(output_dir, f'heatmap_{title}.png'))
    plt.savefig(os.path.join(output_dir, f'heatmap_{title}.svg'), format='svg')
    plt.close()

    # CLUSTERMAP
    clustermap = sns.clustermap(reordered_matrix, 
                                xticklabels=sorted_filenames, 
                                yticklabels=sorted_filenames, 
                                cmap='viridis', 
                                annot=False,
                                fmt=".2f", 
                                figsize=(15, 12),
                                dendrogram_ratio=(.1, .2),
                                cbar_pos=(0, .2, .03, .4),
                                cbar_kws={'label': 'Distancia'})

    final_xticklabels = [label.get_text() for label in clustermap.ax_heatmap.get_xticklabels()]
    final_yticklabels = [label.get_text() for label in clustermap.ax_heatmap.get_yticklabels()]

    final_xcolors = [category_colors[get_category(name)] for name in final_xticklabels]
    final_ycolors = [category_colors[get_category(name)] for name in final_yticklabels]

    for label, color in zip(clustermap.ax_heatmap.get_xticklabels(), final_xcolors):
        label.set_fontsize(6)
        label.set_color('black')
        label.set_bbox(dict(facecolor=color, edgecolor='none', boxstyle='round,pad=0.2'))

    for label, color in zip(clustermap.ax_heatmap.get_yticklabels(), final_ycolors):
        label.set_fontsize(6)
        label.set_color('black')
        label.set_bbox(dict(facecolor=color, edgecolor='none', boxstyle='round,pad=0.2'))

    plt.title(f"Clustermap de {title}", pad=80)
    plt.savefig(os.path.join(output_dir, f'clustermap_{title}.png'))
    plt.savefig(os.path.join(output_dir, f'clustermap_{title}.svg'), format='svg')
    plt.close()

def crear_visualizaciones(ruta_directorio):
    carpeta_visualizacion = os.path.join(ruta_directorio, "visualizacion")
    os.makedirs(carpeta_visualizacion, exist_ok=True)

    archivos_csv = [f for f in os.listdir(ruta_directorio) if f.endswith('.csv')]

    if not archivos_csv:
        print("No se encontraron archivos CSV en el directorio especificado.")
        return

    for archivo in archivos_csv:
        nombre_base = clean_filename(os.path.splitext(archivo)[0])
        distancias = pd.read_csv(os.path.join(ruta_directorio, archivo), index_col=0)

        if distancias.shape[0] != distancias.shape[1]:
            print(f"Advertencia: La matriz de {archivo} no es cuadrada. Se omitirá este archivo.")
            continue

        filenames = list(distancias.columns)
        plot_heatmap_and_clustermap(distancias.values, filenames, nombre_base, carpeta_visualizacion)

    print("Las visualizaciones se han guardado en la carpeta 'visualizacion'.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ruta_directorio = sys.argv[1]
        crear_visualizaciones(ruta_directorio)
    else:
        print("Por favor, especifica la ruta del directorio que contiene las matrices de distancia.")
