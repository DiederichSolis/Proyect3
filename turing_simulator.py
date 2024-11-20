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

   