from config_loader import load_turing_machine_config
from turing_machine_model import TuringMachine

def main(yaml_file):
    """
    Función principal para simular Máquinas de Turing
    """
    # Cargar configuración
    config = load_turing_machine_config(yaml_file)
    
    # Verificar si la configuración se cargó correctamente
    if not config:
        return
    
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

    op = input("que tipo de máquina desea ejecutar? (1. Normal) (2. Alteradora): ")
    
    if(op=="1"):
        main("mt_config.yaml")
    else:
        main("mt_config_alteradora.yaml")
    
