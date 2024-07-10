import threading
import os
import time

def search_keywords_in_file(file_path, keywords, results):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file_path)
    except IOError as e:
        print(f"Error reading {file_path}: {e}")

def thread_worker(file_paths, keywords, results):
    for file_path in file_paths:
        search_keywords_in_file(file_path, keywords, results)

def search_keywords_threading(file_paths, keywords):
    num_threads = 4
    results = {keyword: [] for keyword in keywords}
    threads = []
    chunk_size = len(file_paths) // num_threads
    
    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i != num_threads - 1 else len(file_paths)
        thread = threading.Thread(target=thread_worker, args=(file_paths[start_index:end_index], keywords, results))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return results

keywords = ['be', 'new', 'so']

current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_dir, 'text_files')
file_paths = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.txt')]

start_time = time.time()
threading_results = search_keywords_threading(file_paths, keywords)
end_time = time.time()

print("Threading results:")
for keyword, files in threading_results.items():
    print(f"Word '{keyword}' was found in:")
    for file in files:
        print(file)
    print()

print("Threading execution time:", end_time - start_time)
