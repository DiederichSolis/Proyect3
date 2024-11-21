import yaml

class TuringMachine:
    def __init__(self, config):
        """
        Inicializar la Máquina de Turing con configuración desde YAML
        """
        self.states = config['q_states']['q_list']
        self.initial_state = config['q_states']['initial']
        self.final_state = config['q_states']['final']
        self.input_alphabet = config['alphabet']
        self.tape_alphabet = config['tape_alphabet']
        self.transitions = self._parse_transitions(config['delta'])

    def _parse_transitions(self, delta_config):
        """
        Parsear las funciones de transición del archivo YAML
        """
        transitions = {}
        for transition in delta_config:
            key = (
                transition['params']['initial_state'], 
                transition['params']['tape_input']
            )
            value = {
                'final_state': transition['output']['final_state'],
                'tape_output': transition['output']['tape_output'],
                'tape_displacement': transition['output']['tape_displacement']
            }
            transitions[key] = value
        return transitions

    def simulate(self, input_string):
        """
        Simular una cadena de entrada en la máquina de Turing
        """
        # Preparar la cinta con la cadena de entrada y espacios en blanco
        tape = list(input_string) + ['_'] * len(input_string)
        head_position = 0
        current_state = self.initial_state
        
        # Lista para almacenar descripciones instantáneas
        instantaneous_descriptions = []

        while True:
            # Registrar descripción instantánea actual
            id_current = {
                'state': current_state, 
                'tape': tape.copy(), 
                'head_position': head_position
            }
            instantaneous_descriptions.append(id_current)

            # Verificar si estamos en estado final
            if current_state == self.final_state:
                return {
                    'result': 'Accepted',
                    'ids': instantaneous_descriptions
                }

            # Leer símbolo actual de la cinta
            current_symbol = tape[head_position] if head_position < len(tape) else '_'

            # Buscar transición
            transition_key = (current_state, current_symbol)
            if transition_key not in self.transitions:
                return {
                    'result': 'Rejected',
                    'ids': instantaneous_descriptions
                }

            # Realizar transición
            transition = self.transitions[transition_key]
            current_state = transition['final_state']
            
            # Modificar cinta
            tape[head_position] = transition['tape_output']

            # Mover cabezal
            if transition['tape_displacement'] == 'R':
                head_position += 1
                # Extender cinta si es necesario
                if head_position >= len(tape):
                    tape.append('_')
            elif transition['tape_displacement'] == 'L':
                head_position = max(0, head_position - 1)

def load_turing_machine_config(yaml_file):
    """
    Cargar configuración de Máquina de Turing desde archivo YAML
    """
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main(yaml_file):
    """
    Función principal para simular Máquinas de Turing
    """
    # Cargar configuración
    config = load_turing_machine_config(yaml_file)
    
    # Crear Máquina de Turing
    tm = TuringMachine(config)
    
    # Simular cada cadena de entrada
    for input_string in config['simulation_strings']:
        print(f"\nSimulando cadena: {input_string}")
        result = tm.simulate(input_string)
        
        print(f"Resultado: {result['result']}")
        print("Descripciones Instantáneas:")
        for idx, id_desc in enumerate(result['ids'], 1):
            print(f"ID {idx}: Estado {id_desc['state']}, "
                  f"Cinta: {''.join(id_desc['tape'])}, "
                  f"Posición Cabezal: {id_desc['head_position']}")

if __name__ == "__main__":
    main("mt_config.yaml")