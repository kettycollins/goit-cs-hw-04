import os
import time
import multiprocessing
from collections import defaultdict

def search_keywords_in_file(file_path, keywords, results_queue):
    try:
        result = defaultdict(list)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    result[keyword].append(file_path)
        results_queue.put(result)
    except IOError as e:
        print(f"Error reading {file_path}: {e}")

def process_files(file_list, keywords, results_queue):
    for file_path in file_list:
        search_keywords_in_file(file_path, keywords, results_queue)

def search_keywords_multiprocessing(file_paths, keywords):
    num_processes = 4
    results_queue = multiprocessing.Queue()
    processes = []

    chunk_size = len(file_paths) // num_processes
    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i != num_processes - 1 else len(file_paths)
        chunk = file_paths[start_index:end_index]
        p = multiprocessing.Process(target=process_files, args=(chunk, keywords, results_queue))
        processes.append(p)
        p.start()

    results = defaultdict(list)
    for _ in range(num_processes):
        result = results_queue.get()
        for keyword, files in result.items():
            results[keyword].extend(files)

    for p in processes:
        p.join()

    return results

if __name__ == '__main__':
    keywords = ['be', 'new', 'so']

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, 'text_files')
    file_paths = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.txt')]

    start_time = time.time()
    multiprocessing_results = search_keywords_multiprocessing(file_paths, keywords)
    end_time = time.time()

    print("Multiprocessing results:")
    for keyword, files in multiprocessing_results.items():
        print(f"Word '{keyword}' was found in:")
        for file in files:
            print(file)
        print()

    print("Multiprocessing execution time:", end_time - start_time)
