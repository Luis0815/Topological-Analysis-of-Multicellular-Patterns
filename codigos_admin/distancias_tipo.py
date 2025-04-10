#!/usr/bin/env python3
import os
import sys
import pandas as pd
import numpy as np
import gudhi as gd
import gudhi.wasserstein as gw

def distancias_por_tipo(ruta_directorio):
    carpeta_salida = os.path.join(ruta_directorio, "distancias_por_tipo")
    os.makedirs(carpeta_salida, exist_ok=True)
    
    diagramas_persistencia_A = {}
    diagramas_persistencia_B = {}
    diagramas_persistencia_A_0 = {}
    diagramas_persistencia_B_0 = {}
    
    archivos_csv = [f for f in os.listdir(ruta_directorio) if f.endswith('.csv')]
    
    for archivo_csv in archivos_csv:
        try:
            ruta_completa = os.path.join(ruta_directorio, archivo_csv)
            df = pd.read_csv(ruta_completa, header=0)
            
            if 'birth' not in df.columns or 'death' not in df.columns:
                print(f"El archivo {archivo_csv} no contiene las columnas 'birth' o 'death'.")
                continue
            
            df['birth'] = df['birth'].astype(float)
            df['death'] = df['death'].astype(float)
            
            diag_1 = df[df['dimension'] == 1][['birth', 'death']].to_numpy()
            diag_0 = df[df['dimension'] == 0][['birth', 'death']].to_numpy()
            
            if '_A' in archivo_csv:
                diagramas_persistencia_A[archivo_csv] = diag_1
                diagramas_persistencia_A_0[archivo_csv] = diag_0
            elif '_B' in archivo_csv:
                diagramas_persistencia_B[archivo_csv] = diag_1
                diagramas_persistencia_B_0[archivo_csv] = diag_0
        except Exception as e:
            print(f"Error al procesar el archivo {archivo_csv}: {e}")
    
    def calcular_distancias(diagramas, diagramas_0, nombre_tipo):
        archivos = list(diagramas.keys())
        n = len(archivos)
        tolerancia = 1e-10
        
        distancias_bottleneck_dim1 = np.zeros((n, n))
        distancias_bottleneck_dim0 = np.zeros((n, n))
        distancias_wasserstein_dim1 = np.zeros((n, n))
        distancias_wasserstein_dim0 = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i, n):
                archivo_i = archivos[i]
                archivo_j = archivos[j]
                diag_i = diagramas[archivo_i]
                diag_j = diagramas[archivo_j]
                diag_i_0 = diagramas_0[archivo_i]
                diag_j_0 = diagramas_0[archivo_j]
                
                distancia_bottleneck = gd.bottleneck_distance(diag_i, diag_j)
                distancia_bottleneck_0 = gd.bottleneck_distance(diag_i_0, diag_j_0)
                distancia_wasserstein = gw.wasserstein_distance(diag_i, diag_j, order=1)
                distancia_wasserstein_0 = gw.wasserstein_distance(diag_i_0, diag_j_0, order=1)
                
                distancias_bottleneck_dim1[i, j] = distancias_bottleneck_dim1[j, i] = distancia_bottleneck
                distancias_bottleneck_dim0[i, j] = distancias_bottleneck_dim0[j, i] = distancia_bottleneck_0
                distancias_wasserstein_dim1[i, j] = distancias_wasserstein_dim1[j, i] = distancia_wasserstein
                distancias_wasserstein_dim0[i, j] = distancias_wasserstein_dim0[j, i] = distancia_wasserstein_0
                
                if i == j:
                    if distancia_bottleneck < tolerancia and distancia_wasserstein < tolerancia:
                        print(f"Distancias (Dim 1) para {archivo_i} ({nombre_tipo}) son efectivamente cero.")
                    if distancia_bottleneck_0 < tolerancia and distancia_wasserstein_0 < tolerancia:
                        print(f"Distancias (Dim 0) para {archivo_i} ({nombre_tipo}) son efectivamente cero.")
        
        pd.DataFrame(distancias_bottleneck_dim1, index=archivos, columns=archivos).to_csv(
            os.path.join(carpeta_salida, f'distancias_bottleneck_dim1_{nombre_tipo}.csv'))
        pd.DataFrame(distancias_bottleneck_dim0, index=archivos, columns=archivos).to_csv(
            os.path.join(carpeta_salida, f'distancias_bottleneck_dim0_{nombre_tipo}.csv'))
        pd.DataFrame(distancias_wasserstein_dim1, index=archivos, columns=archivos).to_csv(
            os.path.join(carpeta_salida, f'distancias_wasserstein_dim1_{nombre_tipo}.csv'))
        pd.DataFrame(distancias_wasserstein_dim0, index=archivos, columns=archivos).to_csv(
            os.path.join(carpeta_salida, f'distancias_wasserstein_dim0_{nombre_tipo}.csv'))
    
    if diagramas_persistencia_A:
        print("Calculando distancias para Tipo A...")
        calcular_distancias(diagramas_persistencia_A, diagramas_persistencia_A_0, 'A')
    
    if diagramas_persistencia_B:
        print("Calculando distancias para Tipo B...")
        calcular_distancias(diagramas_persistencia_B, diagramas_persistencia_B_0, 'B')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ruta_directorio = sys.argv[1]
        distancias_por_tipo(ruta_directorio)
    else:
        print("Por favor, especifica la ruta del directorio que contiene los diagramas de persistencia.")
