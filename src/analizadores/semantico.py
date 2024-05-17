
class Variable:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, ast):
        for node in ast:
            if node["type"] == "assignment":
                variable_name = node["variable"]
                value_node = node["value"]

                # Verificar si la variable ya está definida
                if variable_name in self.symbol_table:
                    print(f"Error semántico: Variable '{variable_name}' ya está definida.")
                    return False

                # Analizar el valor asignado
                value = self.analyze_value(value_node)
                if value is not None:
                    self.symbol_table[variable_name] = Variable(variable_name, value)
                else:
                    print(f"Error semántico: Valor no válido para la variable '{variable_name}'.")
                    return False
            elif node["type"] == "usage":
                variable_name = node["variable"]

                # Verificar si la variable está definida
                if variable_name not in self.symbol_table:
                    print(f"Error semántico: Variable '{variable_name}' no está definida.")
                    return False

        return True

    def analyze_value(self, node):
        if node["type"] == "number":
            return node["value"]
        elif node["type"] == "variable":
            variable_name = node["name"]

            # Verificar si la variable está definida
            if variable_name in self.symbol_table:
                return self.symbol_table[variable_name].value
            else:
                print(f"Error semántico: Variable '{variable_name}' no está definida.")
                return None

# Ejemplo de AST (Abstract Syntax Tree)
ast = [
    {"type": "assignment", "variable": "x", "value": {"type": "number", "value": "y"}},
    {"type": "assignment", "variable": "y", "value": {"type": "variable", "name": "x"}},
    {"type": "usage", "variable": "y"},
    {"type": "usage", "variable": "x"}  # Variable no definida
]

# Crear un analizador semántico
analyzer = SemanticAnalyzer()

# Analizar el AST
result = analyzer.analyze(ast)
if result:
    print("Análisis semántico completado con éxito.")
else:
    print("Análisis semántico fallido.")
