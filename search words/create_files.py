from faker import Faker
import os

def create_text_files(num_files, num_words_per_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    fake = Faker()
    
    for i in range(num_files):
        file_path = os.path.join(output_dir, f'text_file_{i+1}.txt')
        with open(file_path, 'w') as file:
            words = ' '.join(fake.words(num_words_per_file))
            file.write(words)

num_files = 10
num_words_per_file = 1000
current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_dir, 'text_files')

create_text_files(num_files, num_words_per_file, output_dir)
