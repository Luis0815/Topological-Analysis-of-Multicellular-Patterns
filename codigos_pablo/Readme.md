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
  
---

##  Paso 2: Calcular distancias entre diagramas de persistencia

El archivo `calcular_distancias.py` permite calcular automáticamente las distancias entre todos los pares de diagramas de persistencia generados en el Paso 1. Se calculan tanto:

- **Distancias de Bottleneck** (dimensiones 0 y 1).
- **Distancias de Wasserstein** (dimensiones 0 y 1).

Los resultados se guardan como matrices de distancias en formato `.csv`.

###  Uso

```bash
python calcular_distancias.py /ruta/a/la/carpeta/persistencia/
```

---

##  Paso 3: Crear visualizaciones de Heatmap y Clustermap

El archivo `crear_visualizaciones.py` permite generar automáticamente **Heatmaps** y **Clustermaps** a partir de las matrices de distancias generadas en el Paso 2. Estas visualizaciones proporcionan una representación gráfica de las distancias entre los diferentes diagramas de persistencia.

###  Uso

```bash
python crear_visualizaciones.py /ruta/a/la/carpeta/distancias/
```
---

# Análisis por grupo celular

Además del análisis general, también es posible realizar el análisis topológico por **grupos de tipos celulares**. Esta segmentación permite observar patrones topológicos propios de distintas funciones inmunológicas o estructurales en el tejido.

Actualmente, se consideran los siguientes grupos celulares:

- **tumorales**: `tumor cells`, `Ki67+ tumor cells`
- **linfoides**: `NK`, `B cells`, `effector CD8+ T cells`, `memory CD8+ T cells`, `CD4+ T cells`, `regulatory T cells`, `memory CD4+ T cells`
- **mieloides**: `neutrophils`, `other APCs`, `dendritic cells`, `M1/M0 macrophages`, `M2 macrophages`
- **no tumorales**: `endothelial cells`, `stromal cells`

##  Paso 1: Calcular complejos de Rips y diagramas de persistencia

Puedes ejecutar el script `rips_por_grupo.py`, que filtra automáticamente las células por grupo y genera los respectivos:

- **Diagramas de persistencia (dim 0 y 1)**
- **Visualización del complejo de Rips**
- **Archivos `.csv` con los datos de persistencia por grupo**

### Uso

```bash
python rips_por_grupo.py /ruta/a/centroides/

