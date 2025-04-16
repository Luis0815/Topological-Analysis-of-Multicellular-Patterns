# Topological-Analysis-of-Multicellular-Patterns
Código y datos para analizar patrones multicelulares mediante TDA. Se estudia la formación de estructuras por adhesión celular y, por separado, se aplica el análisis a datos histológicos de distintos estadios del cáncer para explorar su organización espacial.

### Objetivos Principales:
1. **Estudiar los efectos de la adhesión célula-célula** en la formación de patrones en sistemas multicelulares.
2. **Clasificar la disposición espacial** de distintos tipos celulares usando características topológicas extraídas a través del TDA.
3. **Aplicar TDA a diversos conjuntos de datos**, incluyendo etapas de progresión del cáncer, para investigar cómo la disposición celular en estas etapas se correlaciona con la progresión de la enfermedad.

### Metodología:
El pipeline incluye los siguientes pasos:
- Extracción de los centróides de las ubicaciones celulares a partir de imágenes de muestras de tejido.
- Cálculo de **complejos de Rips** y **homología persistente** a partir de estos datos espaciales.
- Análisis de diagramas de persistencia utilizando las distancias de ***Wasserstein** para comparar diferentes patrones.
- Visualización de los resultados para interpretar las relaciones espaciales entre tipos celulares en diferentes etapas del desarrollo tumoral.

### Conjuntos de Datos:
- Datos simulados variando la adhesion celular.
- Datos extraídos de imágenes de cáncer incluyendo carcinoma, displasia de alto grado y sus respectivas regiones de estroma adyacente.

---

### Estructura del Repositorio y Uso

El repositorio se organiza en carpetas que agrupan los scripts de análisis y los conjuntos de datos. A continuación se describen las carpetas principales:

#### 📁 `codigos_admin/`  
Contiene los scripts necesarios para procesar los datos simulados generados con CompuCell3D. Incluye:
- Conversión de archivos `.vtk` a `.csv`.  
- Separación de datos por tipo celular (azul y rojo).  
- Cálculo de diagramas de persistencia y distancias topológicas.  
- Análisis y visualización de agrupamientos mediante TDA.  

Cada subcarpeta incluye un `README.md` con instrucciones para ejecutar los scripts paso a paso.

#### 📁 `codigos_pablo/`  
Contiene scripts para el análisis de datos histológicos reales. Estos scripts permiten:
- Procesar coordenadas celulares contenidas en archivos `.csv`.  
- Aplicar TDA a muestras con hasta 18 tipos celulares distintos.  
- Clasificar la organización espacial de distintas condiciones (carcinoma, displasia y regiones adyacentes).  

Cada subcarpeta también contiene un `README.md` con instrucciones específicas de uso.

#### 📁 `datos_admin/`  
Incluye los datos simulados desde CompuCell3D:
- Archivos `.vtk` originales.  
- Archivos `.csv` con coordenadas celulares (todas las células, tipo azul, tipo rojo).  
- Subcarpetas con los resultados del análisis TDA y clustering para cada conjunto.

#### 📁 `datos_pablo/`  
Contiene datos derivados de imágenes histológicas:
- Archivos `.csv` con coordenadas celulares, clasificados por muestra.  
- Grupos de datos que incluyen carcinoma, displasia y sus zonas adyacentes.  
- Subcarpetas con los resultados del análisis TDA y clustering para cada conjunto.

---


## Bibliografía

1. **Topological Data Analysis of Spatial Patterning in Heterogeneous Cell Populations: Clustering and Sorting with Varying Cell-Cell Adhesion**  
   [Nature Scientific Reports](https://www.nature.com/articles/s41540-023-00302-8)
   
2. **Persistent Homology Based Characterization of the Breast Cancer Immune Microenvironment: A Feasibility Study**  
   [Dagstuhl Reports](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2020.11)
   
3. **An Introduction to Topological Data Analysis: Fundamental and Practical Aspects for Data Scientists**  
   [Semantic Scholar](https://www.semanticscholar.org/reader/aff16209e232d38fc94a5b0c72067b88d106453f)
   
4. **Comparison of Persistence Diagrams**  
   [arXiv](https://ar5iv.labs.arxiv.org/html/2003.01352)
