import yaml

def load_config(file_path) -> dict | None:
    try:
        with open(file_path, 'r') as f:
            # 加载 YAML 内容
            config = yaml.safe_load(f)
            return config
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None
