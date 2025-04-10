import os
import subprocess
import tarfile

# Definir el tamaño máximo permitido (100MB en bytes)
MAX_SIZE = 100 * 1024 * 1024  # 100 MB en bytes

# Función para comprimir los archivos grandes
def comprimir_archivo(archivo):
    # Definir el nombre del archivo comprimido
    archivo_comprimido = f"{archivo}.tar.gz"
    
    with tarfile.open(archivo_comprimido, "w:gz") as tar:
        tar.add(archivo, arcname=os.path.basename(archivo))
    
    print(f"Archivo {archivo} comprimido como {archivo_comprimido}")
    return archivo_comprimido

# Función para añadir archivos al .gitignore
def actualizar_gitignore(archivo):
    with open(".gitignore", "a") as gitignore:
        gitignore.write(f"{archivo}\n")
    print(f"Archivo {archivo} añadido a .gitignore")

# Función para procesar los archivos
def procesar_archivos():
    archivos = [f for f in os.listdir() if os.path.isfile(f)]
    
    for archivo in archivos:
        # Verificar el tamaño del archivo
        if os.path.getsize(archivo) > MAX_SIZE:
            print(f"Archivo {archivo} supera los 100MB, comprimiendo...")
            archivo_comprimido = comprimir_archivo(archivo)
            # Añadir el archivo comprimido a .gitignore
            actualizar_gitignore(archivo)
            
            # # Eliminar el archivo original (opcional)
            # os.remove(archivo)
            # print(f"Archivo original {archivo} eliminado.")
        else:
            print(f"Archivo {archivo} es de tamaño adecuado.")

# Función para realizar commit y push al repositorio
def git_commit_y_push():
    # Añadir todos los cambios al staging
    subprocess.run(["git", "add", "."])
    
    # Realizar commit
    commit_message = "Actualizar"
    subprocess.run(["git", "commit", "-m", commit_message])
    
    # Hacer push al repositorio remoto
    subprocess.run(["git", "push", "origin", "main"])  

# Función principal
def main():
    procesar_archivos()
    git_commit_y_push()

if __name__ == "__main__":
    main()
