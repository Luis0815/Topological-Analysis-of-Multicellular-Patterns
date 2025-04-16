# Análisis TDA en Datos Histológicos 

Esta carpeta contiene los scripts para aplicar Análisis Topológico de Datos (TDA) a muestras histológicas, utilizando coordenadas celulares extraídas de imágenes. El análisis se realiza a partir de archivos `.csv` que contienen las posiciones de las células y sus respectivos fenotipos.

---

##  Requisitos del archivo de entrada

Antes de ejecutar los scripts, asegurate de que tus archivos `.csv` tengan las siguientes columnas:

| X_centroid | Y_centroid | phenotype           |
|------------|------------|---------------------|
| 123.4      | 567.8      |     tumor cells     | 
| 234.5      | 678.9      | 	M2 macrophages    |
| ...        | ...        | ...                 |

---

##  Paso 1: Calcular complejos de Rips y diagramas de persistencia

El archivo `rips.py` permite generar automáticamente:

- La visualización del **complejo de Rips**.
- El **diagrama de persistencia** (dimensiones 0 y 1).
- Archivos .csv con los datos de persistencia en tres columnas:
  - dimension: dimensión topológica (0 o 1),
  - birth: instante de nacimiento de la característica,
  - death: instante de desaparición de la característica.


###  Uso
```bash
python rips.py /ruta/a/la/carpeta_con_csvs/
```
> ⚠️ **IMPORTANTE:** si tus columnas tienen nombres distintos, deberás modificar las líneas correspondientes en el script `rips.py`:
```python
centroides_x = df['X_centroid'].tolist()
centroides_y = df['Y_centroid'].tolist()
```
* Actualmente se calcula hasta dimensión 2, pero se puede ajustar:
```python
simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)
```
* Radio máximo de conexión por defecto se usa 200. También puede ajustarse:
```python
rips_complex = gd.RipsComplex(points=puntos, max_edge_length=200)
```
  
