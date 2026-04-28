from configparser import ConfigParser
import os

def load_config(filename='database.ini', section='postgresql'):
    # Получаем путь к директории где находится config.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    
    parser = ConfigParser()
    parser.read(file_path)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, file_path))

    return config

if __name__ == '__main__':
    config = load_config()
    print(config)