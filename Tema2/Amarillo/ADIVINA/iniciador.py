import yaml

archivo = "animales.yml"

animales = []
caracteristicas = []

print("\n-------------------------- I N I C I A D O R --------------------------\n")
print("\nIngresa 10 animales y 10 características\n")

# Ingreso de animales
print("\nANIMALES\n")
for i in range(10):
    dato = input(f" Animal {i+1}: ")
    animales.append(dato)

# Ingreso de características
print("\nCARACTERÍSTICAS\n")
for i in range(10):
    dato = input(f" Característica {i+1}: ")
    caracteristicas.append(dato)

# Crear estructura
datos = {
    "Animales": animales,
    "Caracteristicas": caracteristicas
}

# Guardar en YAML
with open(archivo, "w") as f:
    yaml.dump(datos, f, default_flow_style=False, allow_unicode=True)

print(f"\n---------DATOS GUARDADOS EN {archivo}-------------------\n")
