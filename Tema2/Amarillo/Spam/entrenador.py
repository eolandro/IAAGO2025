from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True  # Mantiene las comillas
yaml.width = 1000            # Evita saltos de línea automáticos

# Cargar YAML original
with open("mensajes.yaml", 'r', encoding='utf-8') as entrada:
    Datos = yaml.load(entrada)

# Clasificación manual
clasificados = []
for msj in Datos['mensajes']:
    R = input(f'¿El Mensaje: "{msj}" es Spam? (s/n) => ')
    if R.strip().lower() == 's':
        clasificados.append({msj: True})
    else:
        clasificados.append({msj: False})

# Reemplazar la lista original
Datos['mensajes'] = clasificados

# Guardar YAML en una sola línea por mensaje
with open("msjetq.yaml", 'w', encoding='utf-8') as salida:
    yaml.dump(Datos, salida)


print("\n" + "=" * 30)
print("     Mensajes Clasificados     ")
print("=" * 30,"\n") 
