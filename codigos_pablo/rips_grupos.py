#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gudhi as gd
import argparse
from tqdm import tqdm  

def calcular_rips_por_grupo(ruta_centroides):
    ruta_persistencia = os.path.join(ruta_centroides, "persistencia_grupos_2_900")
    if not os.path.exists(ruta_persistencia):
        os.makedirs(ruta_persistencia)
    
    archivos_csv = [archivo for archivo in os.listdir(ruta_centroides) if archivo.endswith('.csv')]
    
    grupos = {
        'tumorales': ['tumor cells', 'Ki67+ tumor cells'],  
        'linfoides': ['NK', 'B cells', 'effector CD8+ T cells', 
                      'memory CD8+ T cells', 'CD4+ T cells', 
                      'regulatory T cells', 'memory CD4+ T cells'],
        'mieloides': ['neutrophils', 'other APCs', 'dendritic cells', 
                      'M1/M0 macrophages', 'M2 macrophages'],
        'no_tumorales': ['endothelial cells', 'stromal cells']
    }

    total_tareas = len(archivos_csv) * len(grupos)
    progreso = tqdm(total=total_tareas, desc="Procesando archivos", unit="tarea")

    for archivo_csv in archivos_csv:
        ruta_completa = os.path.join(ruta_centroides, archivo_csv)
        df = pd.read_csv(ruta_completa)
        
        for grupo, tipos_celulares in grupos.items():
            df_grupo = df[df['phenotype_key'].isin(tipos_celulares)]
            
            if df_grupo.empty:
                progreso.update(1)
                continue
            
            centroides_x = df_grupo['X_centroid'].tolist()
            centroides_y = df_grupo['Y_centroid'].tolist()
            puntos = np.array(list(zip(centroides_x, centroides_y)))
            
            
            rips_complex = gd.RipsComplex(points=puntos, max_edge_length=1000)
            simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)
            
            # Figura Complejo de Rips
            plt.figure(figsize=(12, 6))
            plt.scatter(centroides_x, centroides_y, color='black', label='Centroides')
            for simplex in simplex_tree.get_skeleton(1):
                if len(simplex[0]) == 2:
                    arista = simplex[0]
                    x = [puntos[i][0] for i in arista]
                    y = [puntos[i][1] for i in arista]
                    plt.plot(x, y, color='gray', linestyle='-', linewidth=1)
            plt.xlabel('Coordenada X')
            plt.ylabel('Coordenada Y')
            plt.title(f'Complejo de Rips - {grupo} ({archivo_csv})')
            plt.legend()

            # Guardar imagen del Complejo de Rips
            nombre_imagen_rips = f"{os.path.splitext(archivo_csv)[0]}_{grupo}_complejo_rips.png"
            ruta_imagen_rips = os.path.join(ruta_persistencia, nombre_imagen_rips)
            plt.tight_layout()
            plt.savefig(ruta_imagen_rips)
            plt.close()

            # Calcular persistencia
            diag = simplex_tree.persistence()
            persistencia_aplanada = [[dimension, birth, death] for dimension, (birth, death) in diag]
            diagram_df = pd.DataFrame(persistencia_aplanada, columns=['dimension', 'birth', 'death'])
            
            diagram_df = diagram_df[diagram_df['dimension'] <= 1]
            
            # Guardar CSV con los datos de persistencia
            nombre_diagrama_csv = f"{os.path.splitext(archivo_csv)[0]}_{grupo}.csv"
            ruta_diagrama_csv = os.path.join(ruta_persistencia, nombre_diagrama_csv)
            diagram_df.to_csv(ruta_diagrama_csv, index=False)

            # Figura Diagrama de Persistencia
            plt.figure(figsize=(6, 6))
            colores_dim = {0: 'blue', 1: 'green', 2: 'orange', 3: 'purple'}  # Colores para cada dimensión
            for dim in diagram_df['dimension'].unique():
                sub_df = diagram_df[diagram_df['dimension'] == dim]
                plt.scatter(sub_df['birth'], sub_df['death'], label=f'Dim {dim}', 
                            color=colores_dim.get(dim, 'gray'), alpha=0.7)
            
            # Línea diagonal para la referencia de persistencia trivial
            max_death = max(diagram_df['death'].max(), 1)
            plt.plot([0, max_death], [0, max_death], linestyle='--', color='red', label='Línea diagonal')
            plt.xlabel('Birth')
            plt.ylabel('Death')
            plt.title(f'Diagrama de Persistencia - {grupo} ({archivo_csv})')
            plt.legend()

            # Guardar imagen del Diagrama de Persistencia
            nombre_imagen_persistencia = f"{os.path.splitext(archivo_csv)[0]}_{grupo}_diagrama_persistencia.png"
            ruta_imagen_persistencia = os.path.join(ruta_persistencia, nombre_imagen_persistencia)
            plt.tight_layout()
            plt.savefig(ruta_imagen_persistencia)
            plt.close()

            # Avanzar barra de progreso
            progreso.update(1)
            print(f'[✔] {archivo_csv} - {grupo} procesado. ({progreso.n}/{total_tareas})')

    progreso.close()
    print(" ¡Procesamiento completado!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcular el complejo de Rips y el diagrama de persistencia por grupo celular.")
    parser.add_argument("ruta", type=str, help="Ruta de la carpeta con archivos CSV de centroides")
    
    args = parser.parse_args()
    calcular_rips_por_grupo(args.ruta)
