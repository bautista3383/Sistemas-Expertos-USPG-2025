# OBJETIVO DEL PROGRAMA
"""El objetivo es determinar si una persona es elegible para un préstamo. 
El sistema no parte de los datos de la persona para ver si califica, sino que comienza con el objetivo de "otorgar préstamo" 
y busca de manera retroactiva los requisitos que deben cumplirse para llegar a esa conclusión."""

# Definimos la clase "Regla", donde cada regla tiene condiciones y una conclusión.
class Regla:
    def __init__(self, condiciones, conclusion):
        self.condiciones = condiciones  # Lista de condiciones que deben cumplirse.
        self.conclusion = conclusion    # La conclusión o estado que se obtiene si las condiciones son verdaderas.

# --- Función para el encadenamiento hacia atrás en finanzas ---
def evaluar_credito(objetivo, datos_persona, reglas):
    """
    Función recursiva para determinar si se cumple un objetivo financiero.

    Args:
        objetivo (str): El objetivo que se desea probar (por ejemplo, "prestamo_aprobado").
        datos_persona (set): Un conjunto de los hechos conocidos sobre la persona.
        reglas (list): La lista de reglas del sistema de evaluación.

    Returns:
        bool: True si el objetivo es verdadero, False si no se puede probar.
    """
    
    # Paso 1: Verificamos si el objetivo ya es un hecho conocido sobre la persona.
    # Esta es la base de la recursión.
    if objetivo in datos_persona:
        print(f"  -> El hecho '{objetivo}' es un dato conocido.")
        return True
    
    # Paso 2: Buscamos una regla cuya conclusión sea nuestro objetivo.
    # Recorremos todas las reglas para encontrar una que nos ayude a probarlo.
    print(f"\nVerificando el objetivo: '{objetivo}'...")
    for regla in reglas:
        if regla.conclusion == objetivo:
            print(f"  -> Encontrada una regla para '{objetivo}'. Condiciones a evaluar: {regla.condiciones}")
            
            # Asumimos que la regla es válida hasta que una condición falle.
            todas_las_condiciones_ok = True
            
            # Paso 3: Llamada recursiva para cada condición.
            for condicion in regla.condiciones:
                # Se llama a la función para probar cada condición.
                # Si una de las condiciones no se puede probar, toda la regla falla.
                if not evaluar_credito(condicion, datos_persona, reglas):
                    todas_las_condiciones_ok = False
                    print(f"  -> No se pudo probar la condición '{condicion}'. Fallando la regla.")
                    break  # Salimos del bucle si una condición no se cumple.
            
            # Si todas las condiciones de la regla se cumplen, el objetivo se prueba.
            if todas_las_condiciones_ok:
                print(f"  -> Todas las condiciones para '{objetivo}' se cumplieron. ¡Objetivo probado!")
                return True
                
    # Paso 4: Si ninguna regla puede probar el objetivo y no es un hecho conocido, el objetivo es falso.
    print(f"  -> No se encontró una regla para probar el objetivo '{objetivo}'.")
    return False

# --- Zona de ejecución del programa ---

if __name__ == "__main__":
    # Datos de la persona que solicita el préstamo.
    datos_solicitante = {"historial_credito_bueno", "ingreso_estable", "deudas_bajas"}

    # Reglas del banco para aprobar un préstamo.
    reglas_evaluacion = [
        Regla(["historial_credito_bueno", "ingreso_estable"], "cumple_requisitos_basicos"),
        Regla(["cumple_requisitos_basicos", "deudas_bajas"], "evaluacion_favorable"),
        Regla(["evaluacion_favorable", "garantia_disponible"], "prestamo_aprobado"),
        Regla(["historial_credito_malo"], "prestamo_denegado")
    ]

    # Definimos el objetivo principal que queremos probar.
    objetivo_final = "prestamo_aprobado"

    # Iniciamos el proceso de encadenamiento hacia atrás.
    print("--- INICIANDO EVALUACIÓN DE CRÉDITO ---")
    if evaluar_credito(objetivo_final, datos_solicitante, reglas_evaluacion):
        print(f"\nCONCLUSIÓN: La persona es elegible para el préstamo. Se cumple el objetivo: '{objetivo_final}'.")
    else:
        print(f"\nCONCLUSIÓN: La persona no es elegible para el préstamo. No se pudo probar el objetivo: '{objetivo_final}'.")
    print("--- EVALUACIÓN FINALIZADA ---")