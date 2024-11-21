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
            elif transition['tape_displacement'] == 'N':
                # No movement
                pass
