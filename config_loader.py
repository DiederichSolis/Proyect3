import yaml

def load_turing_machine_config(yaml_file):
    """
    Cargar configuración de Máquina de Turing desde archivo YAML
    """
    try:
        with open(yaml_file, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"Error: Archivo {yaml_file} no encontrado.")
        return None
    except yaml.YAMLError as e:
        print(f"Error al parsear el archivo YAML: {e}")
        return None