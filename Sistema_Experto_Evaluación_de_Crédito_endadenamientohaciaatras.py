class SistemaCredito:
    def __init__(self):
        """Inicializa el sistema experto con reglas y sin redundancias"""
        self.reglas = [
            # Reglas de aprobación
            {'premisas': ['ingresos=altos', 'deudas=bajas'], 'conclusion': 'credito_aprobado'},
            {'premisas': ['historial_credito=bueno', 'empleo=estable'], 'conclusion': 'credito_aprobado'},
            {'premisas': ['garantia=excelente', 'ingresos=medios'], 'conclusion': 'credito_aprobado'},
            {'premisas': ['garantia=suficiente', 'ingresos=medios', 'historial_credito=bueno'], 'conclusion': 'credito_aprobado'},
            
            # Reglas de garantía
            {'premisas': ['propiedades>=2'], 'conclusion': 'garantia=excelente'},
            {'premisas': ['propiedades=1'], 'conclusion': 'garantia=suficiente'},
            {'premisas': ['propiedades=0'], 'conclusion': 'garantia=insuficiente'},
            
            # Reglas de rechazo
            {'premisas': ['historial_credito=malo'], 'conclusion': 'credito_rechazado'},
            {'premisas': ['ingresos=bajos', 'garantia=insuficiente'], 'conclusion': 'credito_rechazado'},
        ]
        
        self.hechos = {}
        self.objetivo_principal = 'credito_aprobado'
        self.categorias = {
            'ingresos': ['altos', 'medios', 'bajos'],
            'deudas': ['altas', 'moderadas', 'bajas'],
            'historial_credito': ['bueno', 'regular', 'malo'],
            'empleo': ['estable', 'inestable'],
            'propiedades': ['0', '1', '2', '3+']  # Se interpretará numéricamente
        }

    def interpretar_valor(self, variable, valor):
        """Convierte valores categóricos a numéricos cuando es necesario"""
        if variable == 'propiedades':
            if valor.endswith('+'):
                return int(valor[:-1]) + 1  # Convierte "3+" a 4
            return int(valor)
        return valor

    def verificar_comparacion(self, premisa):
        """Verifica premisas con operadores de comparación"""
        operadores = ['>=', '<=', '>', '<', '=']
        for op in operadores:
            if op in premisa:
                var, val = premisa.split(op)
                if var in self.hechos:
                    valor_hecho = self.interpretar_valor(var, self.hechos[var])
                    valor_comparar = self.interpretar_valor(var, val)
                    
                    if op == '>=':
                        return valor_hecho >= valor_comparar
                    elif op == '<=':
                        return valor_hecho <= valor_comparar
                    elif op == '>':
                        return valor_hecho > valor_comparar
                    elif op == '<':
                        return valor_hecho < valor_comparar
                    elif op == '=':
                        return valor_hecho == valor_comparar
        return False

    def encadenamiento_atras(self, objetivo):
        """Implementa encadenamiento hacia atrás"""
        # Verificar si el objetivo ya está en los hechos
        if objetivo in self.hechos.values():
            return True
        
        # Buscar reglas que concluyan este objetivo
        reglas_relevantes = [r for r in self.reglas if r['conclusion'] == objetivo]
        
        if not reglas_relevantes:
            return self.preguntar_al_usuario(objetivo)
            
        for regla in reglas_relevantes:
            todas_verificadas = True
            for premisa in regla['premisas']:
                if any(op in premisa for op in ['>=', '<=', '>', '<']):
                    if not self.verificar_comparacion(premisa):
                        todas_verificadas = False
                        break
                elif not self.encadenamiento_atras(premisa):
                    todas_verificadas = False
                    break
            
            if todas_verificadas:
                self.hechos[objetivo.split('=')[0] if '=' in objetivo else objetivo] = \
                    objetivo.split('=')[1] if '=' in objetivo else True
                return True
                
        return False

    def preguntar_al_usuario(self, objetivo):
        """Método para preguntar al usuario sin redundancias"""
        if '=' in objetivo:
            variable, valor = objetivo.split('=')
            if variable in self.categorias:
                print(f"\n¿Cuál es su {variable.replace('_', ' ')}?")
                for i, opcion in enumerate(self.categorias[variable], 1):
                    print(f"{i}. {opcion}")
                
                while True:
                    try:
                        seleccion = int(input("Seleccione una opción: "))
                        if 1 <= seleccion <= len(self.categorias[variable]):
                            respuesta = self.categorias[variable][seleccion-1]
                            self.hechos[variable] = respuesta
                            return respuesta == valor
                        print("Opción inválida. Intente nuevamente.")
                    except ValueError:
                        print("Por favor ingrese un número.")
                return False
                
        print(f"\n¿{objetivo.replace('_', ' ').replace('=', ' ')}? (s/n)")
        respuesta = input().lower()
        
        if respuesta == 's':
            self.hechos[objetivo] = True
            return True
        return False

    def ejecutar(self):
        """Método principal para ejecutar el sistema experto"""
        print("\nSISTEMA EXPERTO PARA APROBACIÓN DE CRÉDITO")
        print("----------------------------------------")
        print("Analizando solicitud...\n")
        
        resultado = self.encadenamiento_atras(self.objetivo_principal)
        
        print("\n=== RESULTADO ===")
        print("✓ Crédito APROBADO" if resultado else "✗ Crédito RECHAZADO")
        
        print("\nHechos determinantes:")
        for variable, valor in self.hechos.items():
            if isinstance(valor, bool):
                print(f"- {variable.replace('_', ' ')}")
            else:
                print(f"- {variable.replace('_', ' ')}: {valor}")

if __name__ == "__main__":
    sistema = SistemaCredito()
    sistema.ejecutar()