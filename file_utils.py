import os

def get_files_in_folder(folder_path, extension='.txt'):
    """
    Получает список файлов с указанным расширением в заданной папке.

    Args:
        folder_path (str): путь к папке, в которой нужно искать файлы.
        extension (str): расширение искомых файлов.

    Returns:
        list: Список путей к файлам, соответствующим расширению, найденных в папке.
              Если папка не существует или произошла ошибка доступа, возвращает пустой список.
    """
    files = []
    for filename in os.listdir(folder_path): # os.listdir возвращает список имен всех файлов и поддиректорий в этой директории
        if filename.endswith(extension) and os.path.isfile(os.path.join(folder_path, filename)): # Объединяет путь к папке и имя файла в полный путь; # Функция проверяет, существует ли путь и является ли он обычным файлом
            files.append(filename)
    return files
        
if __name__ == "__main__":
    files = get_files_in_folder('corpus', '.txt')
    for file in files:
        print(f" - {file}")



def read_text_file(filepath):
    """
    Читает содержимое файла.
    
    Args:
        filename (str): Имя файла.
        
    Returns:
        str: Содержимое файла или None при ошибке открытия.
    """
    try: 
        with open(filepath, 'r', encoding='utf-8') as f: 
            return f.read() 
    except FileNotFoundError: 
            return "Ошибка: Файл не найден" 
    except UnicodeDecodeError: 
        return "Ошибка: Неверная кодировка файла"
    

if __name__ == "__main__":
   
    files = get_files_in_folder('corpus', '.txt')
    print(f"Найдено файлов: {len(files)}")


def read_csv_file(filename):
    """
    Читает CSV файл и возвращает список словарей.

    Args:
        filepath (str): Путь к CSV файлу

    Returns:
        list: Список словарей, где ключи — названия колонок
    """
    data = []
    try:
        with open(filename, "r", encoding='utf-8') as file:
            lines = file.readlines()
                                                 
            headers = lines[0].strip().split(',')
            
            for line_num, line in enumerate(lines[1:], start=2):
                line = line.strip()
                if not line: 
                    continue
                
                values = line.split(',')
                                
                if len(values) != len(headers):
                    continue
                
                row_dict = {}
                for i in range(len(headers)):
                    row_dict[headers[i]] = values[i]
                
                data.append(row_dict)
        
        return data
    except FileNotFoundError:
        print(f"Файл не найден: {filename}")
        return data
    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {e}")
        return data
     

def write_text_file(filepath, content):
    """
    Записывает текст в указанный файл.

    Args:
        filepath (str): Путь к файлу, в который нужно записать текст.
        content (str): Текст, который нужно записать в файл.

    Returns:
        str: "Текст успешно записан в файл", если успешно
        None: если произошла ошибка

    Обработка ошибок:
        В случае ошибок при открытии или записи файла выводится сообщение об ошибке.
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Текст успешно записан в файл '{filepath}'.")
    except IOError as e:
        print(f"Ошибка при записи файла '{filepath}': {e}")

def write_csv_file(filepath, data, headers):
    """
    Записывает данные в CSV файл.

    Args:
        filepath (str): Полный путь к файлу, включая папку и название файла
                       Например: 'results/statistics.csv'
        data (list): Список списков [[val1, val2], [val1, val2], ...]
        headers (list): Список заголовков ['col1', 'col2']

    Returns:
        bool: True если успешно
    """
    try:
        folder = os.path.dirname(filepath)
        os.makedirs(folder, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(','.join(headers) + '\n')
            for row in data:
                f.write(','.join(str(v) for v in row) + '\n')
        return True
    except:
        return False
