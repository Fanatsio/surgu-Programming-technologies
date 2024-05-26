def compare_files(file1_path, file2_path):
    try:
        with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
            file1_content = file1.read()
            file2_content = file2.read()
            
            return file1_content == file2_content
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False

file1_path = "data.txt"
file2_path = "decompressData.txt"

if compare_files(file1_path, file2_path):
    print("Файлы идентичны.")
else:
    print("Файлы отличаются.")
