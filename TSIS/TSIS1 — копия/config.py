from configparser import ConfigParser
import os

def load_config(filename='database.ini', section='postgresql'):
    # Получаем путь к директории где находится config.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    
    # Проверяем существует ли файл
    if not os.path.exists(file_path):
        raise Exception(f"Configuration file '{file_path}' not found!")
    
    parser = ConfigParser()
    parser.read(file_path)
    
    # Проверяем есть ли секция
    if not parser.has_section(section):
        available_sections = parser.sections()
        raise Exception(f"Section '{section}' not found in {file_path}. Available sections: {available_sections}")
    
    # Получаем параметры
    config = {}
    params = parser.items(section)
    for param in params:
        config[param[0]] = param[1]
    
    # Проверяем обязательные параметры
    required_params = ['host', 'database', 'user', 'password']
    missing_params = [p for p in required_params if p not in config]
    if missing_params:
        raise Exception(f"Missing required parameters in section '{section}': {missing_params}")
    
    return config

if __name__ == '__main__':
    try:
        config = load_config()
        print("Configuration loaded successfully:")
        # Скрываем пароль при выводе
        safe_config = config.copy()
        if 'password' in safe_config:
            safe_config['password'] = '***'
        print(safe_config)
    except Exception as e:
        print(f"Error loading configuration: {e}")