#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.display import Image     # Import the Image function from IPython.display to display images in Jupyter environments.
from os import chdir                  # Import chdir from os module to change the current working directory.
from scipy.spatial import Delaunay  # Importar Delaunay
import numpy as np                    # Import numpy library for working with n-dimensional arrays and mathematical operations.
import gudhi as gd                    # Import gudhi library for computational topology and computational geometry.
import matplotlib.pyplot as plt       # Import pyplot from matplotlib for creating visualizations and graphs.
import argparse                       # Import argparse, a standard library for writing user-friendly command-line interfaces.
import seaborn as sns                 # Import seaborn for data visualization; it's based on matplotl.
import requests # Import requests library to make HTTP requests in Python easily.
import pandas as pd
from scipy.spatial.distance import pdist, squareform 
from sklearn.decomposition import PCA
from scipy.spatial import KDTree
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import gudhi as gd
import gudhi.wasserstein as gw
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


def calcular_rips_y_persistencia(ruta_centroides):
    ruta_persistencia = os.path.join(ruta_centroides, "persistencia_180")
    if not os.path.exists(ruta_persistencia):
        os.makedirs(ruta_persistencia)
    archivos_csv = [archivo for archivo in os.listdir(ruta_centroides) if archivo.endswith('.csv')]

    for archivo_csv in archivos_csv:
        ruta_completa = os.path.join(ruta_centroides, archivo_csv)
   
        df = pd.read_csv(ruta_completa)

        centroides_x = df['X_centroid'].tolist()
        centroides_y = df['Y_centroid'].tolist()
        puntos = np.array(list(zip(centroides_x, centroides_y)))

        rips_complex = gd.RipsComplex(points=puntos, max_edge_length=180)
        simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)

        plt.figure(figsize=(36, 15))

        plt.scatter(centroides_x, centroides_y, color='black', label='Centroides')
        for simplex in simplex_tree.get_skeleton(1): 
            if len(simplex[0]) == 2:  
                arista = simplex[0]
                x = [centroides_x[i] for i in arista]
                y = [centroides_y[i] for i in arista]
                plt.plot(x, y, color='gray', linestyle='-', linewidth=1)
        plt.xlabel('Coordenada X')
        plt.ylabel('Coordenada Y')
        plt.title(f'Complejo de Rips ({archivo_csv})')
        plt.legend()

        diag = simplex_tree.persistence()

        persistencia_aplanada = []
        for d in diag:
            dimension, (birth, death) = d
            persistencia_aplanada.append([dimension, birth, death])

        diagram_df = pd.DataFrame(persistencia_aplanada, columns=['dimension', 'birth', 'death'])
        diagram_df = diagram_df[diagram_df['dimension'] <= 1]
        nombre_diagrama_csv = f"{os.path.splitext(archivo_csv)[0]}.csv"
        ruta_diagrama_csv = os.path.join(ruta_persistencia, nombre_diagrama_csv)
        diagram_df.to_csv(ruta_diagrama_csv, index=False)

        print(f'Gráfico de Rips y diagrama de persistencia guardados para {archivo_csv} en {ruta_persistencia}.')



# In[3]:


def distancias(ruta_directorio):
    # Crear la carpeta de salida
    carpeta_salida = os.path.join(ruta_directorio, "distancias")
    os.makedirs(carpeta_salida, exist_ok=True)

    # Almacenar los diagramas de persistencia
    diagramas_persistencia = {}
    diagramas_persistencia_0 = {}

    # Listar todos los archivos CSV en el directorio
    archivos_csv = [f for f in os.listdir(ruta_directorio) if f.endswith('.csv')]

    # Iterar sobre cada archivo CSV
    for archivo_csv in archivos_csv:
        try:
            # Construir la ruta completa del archivo
            ruta_completa = os.path.join(ruta_directorio, archivo_csv)
            
            # Leer el archivo CSV y asignar nombres de columnas
            df = pd.read_csv(ruta_completa, header=0)  # Usar la primera fila como cabecera
            
            # Asegúrate de que el DataFrame tenga las columnas correctas
            if 'birth' not in df.columns or 'death' not in df.columns:
                print(f"El archivo {archivo_csv} no contiene las columnas 'birth' o 'death'.")
                continue
            
            # Convertir columnas 'birth' y 'death' a flotantes
            df['birth'] = df['birth'].astype(float)
            df['death'] = df['death'].astype(float)

            # Almacenar el diagrama de persistencia en dimensión 1
            diag_1 = df[df['dimension'] == 1][['birth', 'death']].to_numpy()
            diagramas_persistencia[archivo_csv] = diag_1
            
            # Almacenar el diagrama de persistencia en dimensión 0
            diag_0 = df[df['dimension'] == 0][['birth', 'death']].to_numpy()
            diagramas_persistencia_0[archivo_csv] = diag_0
            
        except Exception as e:
            print(f"Error al procesar el archivo {archivo_csv}: {e}")

    # Calcular las distancias entre todos los pares de diagramas de persistencia
    archivos = list(diagramas_persistencia.keys())
    n = len(archivos)
    tolerancia = 1e-10  # Tolerancia para considerar distancias efectivamente como cero

    # Inicializar matrices de distancias
    distancias_bottleneck_dim1 = np.zeros((n, n))
    distancias_bottleneck_dim0 = np.zeros((n, n))
    distancias_wasserstein_dim1 = np.zeros((n, n))
    distancias_wasserstein_dim0 = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):
            archivo_i = archivos[i]
            archivo_j = archivos[j]
            diag_i = diagramas_persistencia[archivo_i]
            diag_j = diagramas_persistencia[archivo_j]
            diag_i_0 = diagramas_persistencia_0[archivo_i]
            diag_j_0 = diagramas_persistencia_0[archivo_j]
            
            # Calcular distancias de Bottleneck
            distancia_bottleneck = gd.bottleneck_distance(diag_i, diag_j)
            distancia_bottleneck_0 = gd.bottleneck_distance(diag_i_0, diag_j_0)
            
            # Calcular distancias de Wasserstein
            distancia_wasserstein = gw.wasserstein_distance(diag_i, diag_j, order=1)
            distancia_wasserstein_0 = gw.wasserstein_distance(diag_i_0, diag_j_0, order=1)
            
            # Almacenar las distancias en las matrices
            distancias_bottleneck_dim1[i, j] = distancias_bottleneck_dim1[j, i] = distancia_bottleneck
            distancias_bottleneck_dim0[i, j] = distancias_bottleneck_dim0[j, i] = distancia_bottleneck_0
            distancias_wasserstein_dim1[i, j] = distancias_wasserstein_dim1[j, i] = distancia_wasserstein
            distancias_wasserstein_dim0[i, j] = distancias_wasserstein_dim0[j, i] = distancia_wasserstein_0
            
            # Verificar que las distancias para el mismo archivo son efectivamente cero
            if i == j:
                if distancia_bottleneck < tolerancia and distancia_wasserstein < tolerancia:
                    print(f"Distancias (Dimensión 1) para {archivo_i} son efectivamente cero.")
                else:
                    print(f"Distancias (Dimensión 1) para {archivo_i} no son cero: Bottleneck = {distancia_bottleneck}, Wasserstein = {distancia_wasserstein}")
                
                if distancia_bottleneck_0 < tolerancia and distancia_wasserstein_0 < tolerancia:
                    print(f"Distancias (Dimensión 0) para {archivo_i} son efectivamente cero.")
                else:
                    print(f"Distancias (Dimensión 0) para {archivo_i} no son cero: Bottleneck = {distancia_bottleneck_0}, Wasserstein = {distancia_wasserstein_0}")

    # Guardar las matrices de distancias en CSV
    pd.DataFrame(distancias_bottleneck_dim1, index=archivos, columns=archivos).to_csv(os.path.join(carpeta_salida, 'distancias_bottleneck_dim1.csv'))
    pd.DataFrame(distancias_bottleneck_dim0, index=archivos, columns=archivos).to_csv(os.path.join(carpeta_salida, 'distancias_bottleneck_dim0.csv'))
    pd.DataFrame(distancias_wasserstein_dim1, index=archivos, columns=archivos).to_csv(os.path.join(carpeta_salida, 'distancias_wasserstein_dim1.csv'))
    pd.DataFrame(distancias_wasserstein_dim0, index=archivos, columns=archivos).to_csv(os.path.join(carpeta_salida, 'distancias_wasserstein_dim0.csv'))

    print("Los cálculos de distancias se han completado y guardado en la carpeta 'distancias'.")


# In[4]:


def extract_levels(filename):
    # Extraer el número después de "dysplasia" en el nombre del archivo
    parts = filename.replace('.csv', '').split('_')
    for part in parts:
        if part.isdigit():
            return int(part)
    return 0  # En caso de que no se encuentre un número, asignamos 0

def sort_filenames(filenames):
    # Ordenar según el número extraído de los nombres
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

    for archivo in archivos_csv:
        nombre_base = os.path.splitext(archivo)[0]
        
        distancias = pd.read_csv(os.path.join(ruta_directorio, archivo), index_col=0)
        
        # Extraer los nombres de los archivos de las columnas
        filenames = list(distancias.columns)
        
        plot_heatmap_and_clustermap(distancias.values, filenames, nombre_base, carpeta_visualizacion)

    print("Las visualizaciones se han guardado.")



# In[7]:





# In[9]:





# In[10]:





# In[ ]:





# In[ ]:




