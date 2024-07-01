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


import threading
from queue import Queue
import time

# Функція для пошуку ключових слів у файлі
def search_keywords_in_file(filename, keywords, results):
    with open(filename, 'r') as f:
        content = f.read()
        for keyword in keywords:
            if keyword in content:
                results[keyword].append(filename)

# Багатопотокова реалізація
def threaded_search(files, keywords):
    results = {keyword: [] for keyword in keywords}
    threads = []
    
    for file in files:
        thread = threading.Thread(target=search_keywords_in_file, args=(file, keywords, results))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return results

# Використання та вивід результатів багатопотокової функції
keywords = ['Python', 'Java', 'C++']
start_time = time.time()
threaded_results = threaded_search(files, keywords)
end_time = time.time()

print("Threaded results:", threaded_results)
print("Threaded search time:", end_time - start_time)