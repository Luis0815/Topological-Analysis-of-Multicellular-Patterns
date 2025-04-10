#!/usr/bin/env python3

import os
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def extract_levels(filename):
    parts = filename.replace('.csv', '').split('_')
    return [int(parts[0]), int(parts[1]), int(parts[2])]

def sort_filenames(filenames):
    return sorted(filenames, key=extract_levels)

def reorder_matrix(matrix, filenames):
    sorted_filenames = sort_filenames(filenames)
    indices = [filenames.index(name) for name in sorted_filenames]
    reordered_matrix = matrix[np.ix_(indices, indices)]
    return reordered_matrix, sorted_filenames

def plot_heatmap_and_clustermap(matrix, filenames, title, output_dir):
    reordered_matrix, sorted_filenames = reorder_matrix(matrix, filenames)
    
    # Heatmap
    plt.figure(figsize=(15, 12))
    sns.heatmap(reordered_matrix, 
                xticklabels=sorted_filenames, 
                yticklabels=sorted_filenames, 
                cmap='viridis', 
                annot=False,
                fmt=".2f", 
                cbar_kws={'label': 'Distancia'})
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(fontsize=8)
    plt.title(f"Heatmap de {title}")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'heatmap_{title}.png'))
    plt.close()

    # Clustermap
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
    clustermap.ax_heatmap.set_xticklabels(
        clustermap.ax_heatmap.get_xticklabels(), 
        rotation=90, 
        fontsize=6)
    clustermap.ax_heatmap.set_yticklabels(
        clustermap.ax_heatmap.get_yticklabels(), 
        rotation=0, 
        fontsize=6)
    plt.title(f"Clustermap de {title}", pad=80)
    plt.savefig(os.path.join(output_dir, f'clustermap_{title}.png'))
    plt.close()

def crear_visualizaciones(ruta_directorio):
    carpeta_visualizacion = os.path.join(ruta_directorio, "visualizacion")
    os.makedirs(carpeta_visualizacion, exist_ok=True)

    archivos_csv = [f for f in os.listdir(ruta_directorio) if f.endswith('.csv')]
    
    if not archivos_csv:
        print("No se encontraron archivos CSV en el directorio especificado.")
        return

    for archivo in archivos_csv:
        nombre_base = os.path.splitext(archivo)[0]
        
        distancias = pd.read_csv(os.path.join(ruta_directorio, archivo), index_col=0)
        
        # Validar que la matriz es cuadrada
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
