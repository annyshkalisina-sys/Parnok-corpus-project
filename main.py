import os
from file_utils import get_files_in_folder, read_text_file, write_csv_file, read_csv_file
from text_utils import count_words, count_unique_words, calculate_ttr, count_lines, average_word_length, get_longest_word, get_most_common_words



def analyze_single_text(filepath, filename):
    """
    Анализирует один файл и возвращает словарь с результатами.
    
    Args:
        filepath (str): Полный путь к файлу.
        filename (str): Имя файла.
    
    Returns:
        dict: Словарь с результатами анализа.
    """
        
    text = read_text_file(filepath)
          
    word_count = count_words(text)
    unique_word_count = count_unique_words(text)
    ttr = calculate_ttr(text)
    lines = count_lines(text)
    avg_word_len = average_word_length(text)
    longest = get_longest_word(text)
    common_words = get_most_common_words(text)
        
    result = {
        'filename': filename,
        'word count': word_count,
        'unique words': unique_word_count,
        'ttr': ttr,
        'lines': lines,
        'avg_word_length': avg_word_len, 
        'longest words' : longest
        }  
    
    return result




def analyze_corpus(corpus_folder):
    """
    Анализирует все файлы в папке, возвращает список словарей с результатами, выводит прогресс в терминал

    Args:
        corpus_folder (str): Путь к папке с текстами (например, 'corpus')
     Returns:
        new_data (dict): Словарь с результатами.
    """
    data = []
    files = get_files_in_folder(corpus_folder, extension='.txt')

    for filename in files:
     file_path = os.path.join(corpus_folder, filename)
     text = read_text_file(file_path)

     word_count = count_words(text)
     unique_word_count = count_unique_words(text)
     ttr = calculate_ttr(text)
     lines_count = count_lines(text)       
     avg_word_len = average_word_length(text)
     longest = get_longest_word(text)            
         
     data.append([filename, word_count, unique_word_count, f"{ttr:.3f}", lines_count, f"{avg_word_len:.2f}", longest])

    csv_path = 'results/statistics.csv'
    headers = ['filename', 'word count', 'unique words', 'ttr', "lines", 'avg_word_length', 'longest words']
    write_csv_file(csv_path, data, headers)

    new_data = read_csv_file(csv_path)

    print("-" * 70) 
    print("Отчет анализа текстовых файлов корпуса")
    print("-" * 70)


    print("Общая статистика:")
    new_data = read_csv_file(csv_path) 
    print(f"Всего текстов: {len(new_data)}")
    
    total_words = sum(int(row['word count']) for row in new_data)
    print(f"Всего слов: {total_words}")

    total_unique_words = sum(int(row['unique words']) for row in new_data)
    print(f"Уникальных слов: {total_unique_words}")

    average_ttr = sum(float(row['ttr']) for row in new_data) / len(new_data)
    print(f"Средний TTR: {average_ttr:.3f}")
    

    print("Статистика по каждому файлу:") 
    print("-" * 70)
    for row in new_data:
        print(f"Файл: {row['filename']}")
        print(f"Строк: {row['lines']}")
        print(f"Слов: {row['word count']}")
        print(f"Уникальных слов: {row['unique words']}")
        print(f"type-token ratio: {row['ttr']}")
        print(f"Средняя длина слова: {row['avg_word_length']}")
        print(f"Самое длинное слово: {row['longest words']}")
        return new_data
    
             

def generate_report():
    """
    Генерирует текстовый отчёт, объединяет данные анализа с метаданными
    """
        
    os.makedirs('results', exist_ok=True)
    
    data = read_csv_file('results/statistics.csv')
    metadata = read_csv_file('data/metadata.csv')
        
    titles_dict = {}
    if metadata:
        for item in metadata:
            filename = item.get('filename', '')
            title = item.get('title', '')
            if filename and title:
                titles_dict[filename] = title
    else:
        print("Файл metadata.csv не найден или пуст")
    
    with open('results/report.txt', 'w', encoding='utf-8') as f:      
        f.write("-" * 80 + "\n")
        f.write("Анализ корпуса текстов\n")
        f.write("-" * 80 + "\n")
               
        f.write("ОБЩАЯ СТАТИСТИКА:\n")
        
        total_files = len(data)
        f.write(f"Всего текстов: {total_files}\n")
        
        total_words = sum(int(r['word count']) for r in data)
        f.write(f"Всего слов: {total_words}\n")
        
        total_unique = sum(int(r['unique words']) for r in data)
        f.write(f"Уникальных слов: {total_unique}\n")
        
        avg_ttr = sum(float(r['ttr']) for r in data) / total_files
        f.write(f"Средний type-token ratio: {avg_ttr:.3f}\n\n")
       
        f.write("Статистика по отдельным файлам:\n")
        f.write("-" * 70 + "\n")

    
        def file_key(filename):
            try:
                return int(filename.replace('text', '').replace('.txt', ''))
            except:
                return 0
        
        sorted_data = sorted(data, key=lambda x: file_key(x['filename']))

        most_diverse_text = None
        most_diverse_ttr = 0
        most_diverse_title = ""
        
        biggest_lines = None
        littlest_word_count = 0
        biggest_text = ""
        
        shortest_text = None
        shortest_word_count = float('inf')
        shortest_title = ""
                
        for row in sorted_data:
            filename = row['filename']
            title = titles_dict.get(filename, filename)
            ttr = float(row['ttr'])
            word_count_val = int(row['word count'])
                        
            if ttr > most_diverse_ttr:
                most_diverse_ttr = ttr
                most_diverse_text = filename
                most_diverse_title = title
            
            if word_count_val > littlest_word_count:
                littlest_word_count = word_count_val
                biggest_text = filename
                biggest_lines = title
                        
            if word_count_val < shortest_word_count:
                shortest_word_count = word_count_val
                shortest_text = filename
                shortest_title = title
                        
            f.write(f"Текст: {title}\n")
            f.write(f"Файл: {filename}\n")
            f.write(f"Строк: {row['lines']}\n")
            f.write(f"Слов: {row['word count']}\n")
            f.write(f"Уникальных слов: {row['unique words']}\n")
            f.write(f"TTR: {row['ttr']}\n")
            f.write(f"Средняя длина слова: {row['avg_word_length']}\n")
            f.write("\n")
               
        f.write("Итоги:\n")
        
        if most_diverse_title:
            f.write("1. Самый лексически разнообразный текст:\n")
            f.write(f"{most_diverse_title}\n")
            f.write(f"TTR: {most_diverse_ttr:.3f}\n")
            f.write(f"Уникальных слов: {next(r['unique words'] for r in data if r['filename'] == most_diverse_text)}\n")
            f.write(f"Всего слов: {next(r['word count'] for r in data if r['filename'] == most_diverse_text)}\n")
            f.write("\n")
                
        if biggest_text:
            f.write("2. Текст с наибольшим количеством строк:\n")
            f.write(f"{biggest_text}\n")
            f.write(f"Строк: {next(r['lines'] for r in data if r['filename'] == biggest_lines)}\n")
            f.write(f"Всего слов: {next(r['word count'] for r in data if r['filename'] == biggest_text)}\n")
            f.write("\n")


def main():
    """
    Главная функция программы.       
    """
    print("=" * 70)
    print("Все тексты")
    print("=" * 70)
    
    corpus_folder = 'corpus'
        
    if not os.path.exists(corpus_folder):
        print(f"Папка '{corpus_folder}' не найдена")       
        return       
         
    print(f"Поиск файлов в папке '{corpus_folder}'")
    files = get_files_in_folder(corpus_folder, '.txt')  

    print(f"Найдено файлов: {len(files)}")
    print("Список файлов для анализа:")

    for i, filename in enumerate(files, start=1):
        print(f"{i}. {filename}")
        
    analyze_corpus(corpus_folder)
    generate_report()
       
    print("Обработка завершена!")
 
if __name__ == "__main__":
    main()