import time

def monitor_progress():
    progress = 0
    while progress < 100:
        # Simulamos el progreso de alguna tarea
        time.sleep(1)  # Esperar un segundo
        progress += 10  # Actualizamos el progreso
        yield progress  # Devolvemos el progreso actualizado en cada iteración

# Usamos el generador
for current_progress in monitor_progress():
    print(f"Progreso: {current_progress}%")