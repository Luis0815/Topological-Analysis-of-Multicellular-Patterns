#!/bin/bash

# Definir las extensiones de los archivos que quieres comprimir
extensiones=("*.csv" "*.svg" "*.checkpoint")

# Tamaño mínimo de archivo en bytes (100 MB = 100 * 1024 * 1024 bytes)
tamano_minimo=104857600  # 100 MB

# Recorrer todos los archivos que coinciden con las extensiones
for ext in "${extensiones[@]}"; do
    for archivo in $(find . -type f -name "$ext"); do
        # Comprobar el tamaño del archivo
        tamano_archivo=$(stat -c %s "$archivo")
        
        # Si el archivo es mayor que 100 MB, comprimirlo
        if [ "$tamano_archivo" -gt "$tamano_minimo" ]; then
            echo "Comprobando: $archivo (Tamaño: $tamano_archivo bytes)"
            
            # Comprimir el archivo en formato .gz
            gzip -c "$archivo" > "$archivo.gz"
            
            # Añadir los archivos comprimidos a Git
            git add "$archivo.gz"
            
            # Eliminar los archivos originales de la zona de preparación (staging)
            git rm --cached "$archivo"
            
            # Agregar los archivos originales al .gitignore
            echo "$archivo" >> .gitignore
        fi
    done
done

# Hacer commit de los cambios
git add .gitignore
git commit -m "Comprimir archivos grandes y agregar los originales al .gitignore"

