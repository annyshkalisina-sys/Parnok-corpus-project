def count_words(text):
    """
    Подсчитывает количество слов в тексте.

    Args:
        text (str): Текст для анализа

    Returns:
        int: Количество слов
    """
    words = text.split()
    return len(words)



def count_unique_words(text):
    """
    Подсчитывает количество уникальных слов.
    
    Args: 
        words (str): Слова, взятые из текста
        
    Returns:  
        int: Количество уникальных слов 
    """  
    words = text.split()
    unique_words = set(words)
    return len(unique_words)



def calculate_ttr(text):
    """
    Рассчитывает type-token ratio.

    Args:
        text (str): Текст для анализа
        
    Returns:
        float: type-token ratio
    """
    total_words = count_words(text)
    unique_words = count_unique_words(text)
    return unique_words/total_words



def get_most_common_words(text, n=10):
    """
    Возвращает n самых часто встречающихся в тексте слов.
    
    Args:
        text (str): Текст для анализа
        n (int): Количество возвращаемых слов (10)
        
    Returns:
        list: Список кортежей в формате (слово, количество_вхождений)
    """
    from collections import Counter
    word_counter = Counter(text.split())
    return word_counter.most_common(n)



def count_lines(text):
    """
    Подсчитывает количество строк в тексте.
    
    Args: 
        text (str): Текст для анализа

    Returns: 
        int: Количество строк
    """
    lines = text.split('\n')
    return len(lines)



def average_word_length(text):
    """
    Подсчитывает среднюю длину слова в тексте.
    
    Args:
        text (str): Текст для анализа.
        
    Returns:
        float: Средняя длина слова.
    """
    words = text.split()
    total = sum(len(word) for word in words)
    return total/len(words)

def get_longest_word(text):
    """
    Возвращает самое длинное слово (при равенстве — любое из максимальных).

    Args:
        text (str): список слов.

    Returns:
        str: самое длинное слово.
    """
    clean_text = text.lower()
    for punct in ",.!?;:—-":
       clean_text = clean_text.replace(punct, "")
    words = clean_text.split()
    if not words:
        return ''
    return max(words, key=len)