import yaml

class MaquinaDeTuring:
    def __init__(self, configuracion):
        # Cargar configuración inicial desde la nueva estructura YAML
        self.estados = configuracion["q_states"]["q_list"]
        self.estado_inicial = configuracion["q_states"]["initial"]
        self.estado_final = configuracion["q_states"]["final"]
        self.alfabeto = configuracion["alphabet"]
        self.alfabeto_cinta = configuracion["tape_alphabet"]
        # Procesar las transiciones desde el formato de lista a un diccionario
        self.transiciones = {}
        for transicion in configuracion["delta"]:
            clave = (transicion["params"]["initial_state"], transicion["params"]["tape_input"])
            self.transiciones[clave] = (
                transicion["output"]["final_state"],
                transicion["output"]["tape_output"],
                transicion["output"]["tape_displacement"],
            )
        self.cadenas_a_simular = configuracion["simulation_strings"]

        self.estado_actual = self.estado_inicial
        self.cinta = []
        self.posicion_cabeza = 0

    def reiniciar(self, cadena_entrada):
        # Inicializar cinta y posición de la cabeza de lectura
        self.cinta = list(cadena_entrada) + ["_"]
        self.estado_actual = self.estado_inicial
        self.posicion_cabeza = 0

    def ejecutar_paso(self):
        # Obtener el símbolo actual bajo la cabeza de lectura
        simbolo_actual = self.cinta[self.posicion_cabeza]

        # Buscar la transición correspondiente
        clave = (self.estado_actual, simbolo_actual)
        if clave not in self.transiciones:
            return False  # No hay transición válida

        nuevo_estado, simbolo_escribir, movimiento = self.transiciones[clave]

        # Actualizar cinta, estado y posición de la cabeza
        self.cinta[self.posicion_cabeza] = simbolo_escribir
        self.estado_actual = nuevo_estado
        if movimiento == "R":
            self.posicion_cabeza += 1
        elif movimiento == "L":
            self.posicion_cabeza -= 1

        # Asegurar que la cabeza no salga de los límites de la cinta
        if self.posicion_cabeza < 0:
            self.cinta.insert(0, "_")
            self.posicion_cabeza = 0
        elif self.posicion_cabeza >= len(self.cinta):
            self.cinta.append("_")
        return True

    def ejecutar(self, cadena_entrada):
        self.reiniciar(cadena_entrada)
        print(f"Configuración inicial: {self.obtener_configuracion()}")

        while self.estado_actual != self.estado_final:
            if not self.ejecutar_paso():
                print("No se encontró una transición válida. Entrada rechazada.")
                return "Rechazada"
            print(f"Configuración actual: {self.obtener_configuracion()}")

        print("Entrada aceptada.")
        return "Aceptada"

    def obtener_configuracion(self):
        # Devuelve la configuración instantánea (ID)
        cinta_str = "".join(self.cinta)
        marcador_cabeza = " " * self.posicion_cabeza + "^"
        return f"Cinta: {cinta_str}\nCabeza: {marcador_cabeza}\nEstado: {self.estado_actual}"


def cargar_configuracion(ruta_archivo):
    # Cargar archivo YAML
    with open(ruta_archivo, "r") as archivo:
        return yaml.safe_load(archivo)


if __name__ == "__main__":
    # Ruta del archivo YAML
    archivo_yaml = "mt_config.yaml"  # Cambia este nombre por el de tu archivo YAML

    # Cargar configuración de la Máquina de Turing
    configuracion = cargar_configuracion(archivo_yaml)

    # Crear una instancia de la Máquina de Turing
    mt = MaquinaDeTuring(configuracion)

    # Ejecutar las cadenas de prueba
    for cadena_entrada in configuracion["simulation_strings"]:
        print(f"\nEjecutando entrada: {cadena_entrada}")
        resultado = mt.ejecutar(cadena_entrada)
        print(f"Resultado: {resultado}\n")
