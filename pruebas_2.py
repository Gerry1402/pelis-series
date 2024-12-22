from rich.progress import Progress
import time

def process_part(progress, task_id):
    for i in range(5):  # Simula trabajo
        time.sleep(0.2)  # Simula trabajo
        progress.update(task_id, advance=20)

def main():
    total_parts = 3  # Número de partes
    with Progress() as progress:
        # Barra de progreso total
        total_task = progress.add_task("Progreso Total", total=total_parts)
        
        # Crear tareas para cada parte
        part_tasks = [
            progress.add_task(f"Parte {i+1}/{total_parts}", total=100)
            for i in range(total_parts)
        ]
        
        for part_index, task_id in enumerate(part_tasks):
            print(task_id)
            process_part(progress, task_id)  # Procesar la parte
            progress.update(total_task, advance=1)  # Avanzar en el progreso total

if __name__ == "__main__":
    main()