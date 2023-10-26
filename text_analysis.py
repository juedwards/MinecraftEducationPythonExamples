import os
import zipfile
from spellchecker import SpellChecker

def get_file_path():
    file_name = input("Enter the file name (without .mcworld suffix): ") + ".mcworld"
    return os.path.join(os.path.expanduser("~\\Downloads"), file_name)

def ensure_destination_folder(mcworld_file_path):
    destination_folder_path = os.path.splitext(mcworld_file_path)[0]

    if os.path.exists(destination_folder_path):
        proceed = input(f"Folder already exists: {destination_folder_path}\nProceed to delete the folder and all its contents? (y/n): ")
        if proceed.lower() != "y":
            return None

        # Recursively delete the folder
        for root, dirs, files in os.walk(destination_folder_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    
    return destination_folder_path

def extract_mcworld(mcworld_file_path, destination_folder_path):
    with zipfile.ZipFile(mcworld_file_path, "r") as zip_file:
        zip_file.extractall(destination_folder_path)

def find_en_US_lang(destination_folder_path):
    en_US_lang_file_paths = [os.path.join(root, name) for root, _, files in os.walk(destination_folder_path) for name in files if name == "en_US.lang"]
    
    if not en_US_lang_file_paths:
        print("en_US.lang file not found")
        return None

    if len(en_US_lang_file_paths) == 1:
        print(f"ONE en_US.lang file found: {en_US_lang_file_paths[0]}")
        return en_US_lang_file_paths[0]

    print("More than one en_US.lang file found:")
    for path in en_US_lang_file_paths:
        print(path)

    largest_file_path = max(en_US_lang_file_paths, key=os.path.getsize)
    print(f"Largest en_US.lang file found: {largest_file_path}")

    return largest_file_path

def clean_line(line, english_dictionary):
    # Keep only letters and spaces
    clean = ''.join(e for e in line if e.isalpha() or e.isspace())
    
    # Filter out single-letter words and check if the word is in the english_dictionary
    clean = ' '.join([w for w in clean.split() if len(w) > 1 and w in english_dictionary]).strip()

    return clean

def text_analysis(en_US_lang_file_path):
    spell = SpellChecker()
    english_dictionary = set(spell.word_frequency.dictionary.keys())

    try:
        with open(en_US_lang_file_path, "r", encoding="utf-8") as en_US_lang_file:
            en_US_lang_file_contents_array = en_US_lang_file.read().splitlines()
    except Exception as e:
        print("en_US.lang file not found")
        print(en_US_lang_file_path)
        print("Error:",e)
        return

    grade_levels = []
    lines_skipped = 0
    grades_skipped = 0

    # if os.path.join(os.path.dirname(en_US_lang_file_path), "text_analysis.txt" exists, delete it
    if os.path.exists(os.path.join(os.path.dirname(en_US_lang_file_path), "text_analysis.txt")):
        os.remove(os.path.join(os.path.dirname(en_US_lang_file_path), "text_analysis.txt"))

    for line in en_US_lang_file_contents_array:
        cleaned_line = clean_line(line, english_dictionary)
        words = cleaned_line.split()
        num_words = len(words)

        # Treat every line as a sentence
        number_of_sentences = 1

        number_of_syllables = 0
        for word in words:
            number_of_syllables += count_syllables(word)
        
        # calculate the grade level of the string
        grade_level = None  # Initialize with a default value

        if num_words == 0:
            grades_skipped += 1
            grade_level = None
        else:
            grade_level = 0.39 * (num_words / number_of_sentences) + 11.8 * (number_of_syllables / num_words) - 15.59

        if grade_level is not None:
            grade_levels.append(grade_level)

        with open(os.path.join(os.path.dirname(en_US_lang_file_path), "text_analysis.txt"), "a", encoding="utf-8") as text_analysis_file:
            text_analysis_file.write(f"Sentence: {line}\nNumber of words: {num_words}\nNumber of syllables: {number_of_syllables}\nGrade level: {grade_level}\n\n")


    if grade_levels:
        avg_grade = round(sum(grade_levels) / len(grade_levels), 2)
        print(f"Average grade level: {avg_grade}")

    print(f"Lines skipped: {lines_skipped}")
    print(f"Grades not assigned: {grades_skipped}")
    print("Lines: ", len(en_US_lang_file_contents_array))
    print("Analysis stored in text file: ", os.path.join(os.path.dirname(en_US_lang_file_path), "text_analysis.txt"))

def clean_line(line, dictionary):
    line = ''.join(e for e in line if e.isalnum() or e.isspace())
    line = ''.join(e for e in line if not e.isdigit())
    line = ' '.join([w for w in line.split() if len(w)>1 and w in dictionary])
    if "=" in line:
        line = line.split("=")[1]
    return line.strip()

def compute_line_stats(words):
    num_words = len(words)
    num_sentences = sum(1 for word in words if word.endswith(('.', '!', '?')))
    num_syllables = sum(count_syllables(word) for word in words)
    return num_words, num_sentences, num_syllables

def count_syllables(word):
    vowels = "aeiouy"
    count = sum(1 for i in range(len(word)) if word[i] in vowels and (i == 0 or word[i-1] not in vowels))
    count -= word.endswith("e")
    return count or 1

def main():
    mcworld_file_path = get_file_path()
    if not os.path.exists(mcworld_file_path):
        print(f"File not found: {mcworld_file_path}")
        return

    destination_folder_path = ensure_destination_folder(mcworld_file_path)
    if destination_folder_path:
        extract_mcworld(mcworld_file_path, destination_folder_path)
        print(f"Extracted folder: {destination_folder_path}")

        find_us_EN = input("Would you like to find the us_EN.lang file? (y/n): ").lower()
        if find_us_EN == "y":
            path_to_en_US_lang = find_en_US_lang(destination_folder_path)
            if path_to_en_US_lang:
                do_analysis = input("Would you like to carry out text analysis on the en_US.lang file? (y/n): ").lower()
                if do_analysis == "y":
                    spell = SpellChecker()
                    dictionary = set(spell.word_frequency.dictionary.keys())
                    text_analysis(path_to_en_US_lang)

if __name__ == "__main__":
    main()
