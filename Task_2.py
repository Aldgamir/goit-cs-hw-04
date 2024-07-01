import multiprocessing
import time

# Створимо тестові файли для обробки
files = ['file1.txt', 'file2.txt', 'file3.txt']
contents = [
    "Python is a programming language. Python is used for web development as well as application development.",
    "Java is another programming language. Java and Python are popular as well as JS and some others",
    "C++ is a powerful language. Unlike Python, C++ is used for system programming and could named as one of the hardest languages for begginers."
]

for file, content in zip(files, contents):
    with open(file, 'w') as f:
        f.write(content)

# Функція для пошуку ключових слів у файлі (процес)
def search_keywords_in_file_process(filename, keywords, queue):
    result = {keyword: [] for keyword in keywords}
    try:
        with open(filename, 'r') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    result[keyword].append(filename)
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
    queue.put(result)

# Багатопроцесорна реалізація
def multiprocessing_search(files, keywords):
    queue = multiprocessing.Queue()
    processes = []

    for file in files:
        process = multiprocessing.Process(target=search_keywords_in_file_process, args=(file, keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Збір результатів з черги
    final_results = {keyword: [] for keyword in keywords}
    while not queue.empty():
        result = queue.get()
        for keyword, filenames in result.items():
            final_results[keyword].extend(filenames)

    return final_results

# Використання та вивід результатів багатопроцесорної функції
keywords = ['Python', 'Java', 'C++']
start_time = time.time()
multiprocessing_results = multiprocessing_search(files, keywords)
end_time = time.time()

print("Multiprocessing results:", multiprocessing_results)
print("Multiprocessing search time:", end_time - start_time)