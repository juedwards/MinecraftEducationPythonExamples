# Minecraft Educaiton World Text File Analysis for NPC text
# Justin Edwards, Minecraft Educaiton
# @JustinEducation

import os
import zipfile
from spellchecker import SpellChecker

def open_and_convert():
    
    # Get the file name from the user
    file_name = input("Enter the file name (without .mcworld suffix): ")

    # Add the .mcworld suffix to the file name
    file_name += ".mcworld"

    # Get the path to the Downloads folder
    downloads_folder = os.path.expanduser("~\\Downloads")

    # Create the full path to the .mcworld file
    mcworld_file_path = os.path.join(downloads_folder, file_name)

    # Create the full path to the destination folder
    destination_folder_path = os.path.join(downloads_folder, os.path.splitext(file_name)[0])

    #check file exists, if it doesn't inform the user and exit the function
    if not os.path.exists(mcworld_file_path):
        print(f"File not found: {mcworld_file_path}")
        return

    #if the destination folder already exists, inform the user and ask them to proceed to delete it and all its contents.
    if os.path.exists(destination_folder_path):
        print(f"Folder already exists: {destination_folder_path}")
        proceed = input("Proceed to delete the folder and all its contents? (y/n): ")
        if proceed.lower() != "y":
            return
        else:
            # Delete the destination folder and all its contents
            for root, dirs, files in os.walk(destination_folder_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(destination_folder_path)

    # Create a ZipFile object for writing
    zip_file = zipfile.ZipFile(destination_folder_path + ".zip", "w")

    # Add the .mcworld file to the zip file
    zip_file.write(mcworld_file_path, file_name)

    # Close the zip file
    zip_file.close()

    # Create a ZipFile object for reading
    zip_file = zipfile.ZipFile(mcworld_file_path, "r")

    # Extract the contents of the zip file to the destination folder
    zip_file.extractall(destination_folder_path)

    # Close the zip file
    zip_file.close()

    return destination_folder_path

def find_en_US_lang(destination_folder_path):
    #itterate through every folder and subfolder in the destination folder and find any flie named en_US.lang. Append the path to the file to an array called en_US_lang_file_paths
    en_US_lang_file_paths = []
    for root, dirs, files in os.walk(destination_folder_path):
        for name in files:
            if name == "en_US.lang":
                en_US_lang_file_paths.append(os.path.join(root, name))
    
    #if there are no en_US.lang files, inform the user and exit the function
    if len(en_US_lang_file_paths) == 0:
        print("en_US.lang file not found")
        # return nothing
        return None
    
    #if there is one en_US.lang file, print the path to it and exit the function
    if len(en_US_lang_file_paths) == 1:
        print(f"ONE en_US.lang file found: {en_US_lang_file_paths[0]}")
        return en_US_lang_file_paths[0]
    
    # If there is more than one en_US.lang file, inform the user
    if len(en_US_lang_file_paths) > 1:
        print("More than one en_US.lang file found:")
        for path in en_US_lang_file_paths:
            print(path)
        print("Finding the largest en_US.lang file...")
    
    #find the largest en_US.lang file
    largest_file_size = 0
    largest_file_path = ""
    for path in en_US_lang_file_paths:
        file_size = os.path.getsize(path)
        if file_size > largest_file_size:
            largest_file_size = file_size
            largest_file_path = path
    
    #print the path to the largest en_US.lang file
    print(f"Largest en_US.lang file found: {largest_file_path}")
    return largest_file_path

def text_analysis(en_US_lang_file_path):
    #open the en_US.lang file and read the contents into a string
    #split the string into an array of strings, each string being a line in the file
    #for each line in the array, clean the string removing non-english words, punctuation, numbers, etc.
    #itterate through the array and test the grade level of the string using the Flesch-Kincaid Grade Level Test, recording the grade level of each string in a new array
    #calculate the average grade level of the array

    spell = SpellChecker() #create a spellchecker object
    english_dictionary = set(spell.word_frequency.dictionary.keys()) #create a set of all the words in the english dictionary

    #open the en_US.lang file and read the contents into a string, if the file doesn't exist, inform the user and exit the function
    try:
        en_US_lang_file = open(en_US_lang_file_path, "r", encoding="utf-8")
        en_US_lang_file_contents = en_US_lang_file.read()
    except Exception as e:
        print("en_US.lang file not found")
        print(en_US_lang_file_path)
        print("Error:",e)
        return
    
    #split the string into an array of strings, each string being a line in the file
    en_US_lang_file_contents_array = en_US_lang_file_contents.splitlines()

    grade_levels = []  #create an array to store the grade levels of each line in the file
    lines_skipped = 0 #create a variable to store the number of lines skipped

    #for each line in the array, clean the string removing non-english words, punctuation, numbers, etc.
    for line in en_US_lang_file_contents_array:
        #remove non-english words, punctuation, numbers, etc.
        #remove all characters that are not letters, numbers, or spaces
        line = ''.join(e for e in line if e.isalnum() or e.isspace())
        #remove all numbers
        line = ''.join(e for e in line if not e.isdigit())
        #remove all single letter words
        line = ' '.join([w for w in line.split() if len(w)>1])
        #remove all words that are not in the english dictionary
        line = ' '.join([w for w in line.split() if w in english_dictionary])
        #strip all whitespace from each line
        line = line.strip()
        # if a = is present in the line, delete everything before it and the = itself
        if "=" in line:
            line = line.split("=")[1]
        

    #itterate through the array and test the grade level of the string using the Flesch-Kincaid Grade Level Test, recording the grade level of each string in a new array
    for line in en_US_lang_file_contents_array:
        #split the string into an array of words
        words = line.split()
        #count the number of words
        number_of_words = len(words)
        #count the number of sentences
        number_of_sentences = 0
        for word in words:
            if word.endswith(".") or word.endswith("!") or word.endswith("?"):
                number_of_sentences += 1
        #count the number of syllables
        number_of_syllables = 0
        for word in words:
            number_of_syllables += count_syllables(word)
        
        if number_of_sentences == 0:
            print(f"No sentences detected in line: '{line}'. Skipping...")
            lines_skipped += 1
            continue
        
        #calculate the grade level of the string
        grade_level = 0.39 * (number_of_words / number_of_sentences) + 11.8 * (number_of_syllables / number_of_words) - 15.59
        #record the grade level of the string in a new array
        grade_levels.append(grade_level)

        #append the sentence, number of words, number of sentences, number of syllables, and grade level to a text file in the same directory as the en_US.lang file
        try:
            with open(os.path.join(os.path.dirname(en_US_lang_file_path), "text_analysis.txt"), "a", encoding="utf-8") as text_analysis_file:
                text_analysis_file.write(f"Sentence: {line}\nNumber of words: {number_of_words}\nNumber of sentences: {number_of_sentences}\nNumber of syllables: {number_of_syllables}\nGrade level: {grade_level}\n\n")
        except Exception as e:
            print("Error:",e)
            return
    
    #calculate the average grade level of the array
    average_grade_level = sum(grade_levels) / len(grade_levels)
    # round average_grade_level to 2 decimal places
    average_grade_level = round(average_grade_level, 2)

    print(f"Average grade level: {average_grade_level}")
    print(f"Lines skipped: {lines_skipped}")
    print("Lines: ", len(en_US_lang_file_contents_array))
    print("Analysis stores in text file: ", os.path.join(os.path.dirname(en_US_lang_file_path), "text_analysis.txt"))

def count_syllables(word):
    word = word.lower()
    vowels = "aeiouy"
    count = 0

    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count






# open and convert the .mcworld file to a .zip file and extract, saving the path to the extracted folder
destination_folder_path = open_and_convert()
# if destination_folder_path is not "" then print the path to the extracted folder
if destination_folder_path:
    print(f"Extracted folder: {destination_folder_path}")
#ask the user if they would like to find the us_EN.lang file
find_us_EN = input("Would you like to find the us_EN.lang file? (y/n): ")
#if the user would like to find the en_US.lang file, then call the function to find it
if find_us_EN.lower() == "y":
    path_to_en_US_lang = find_en_US_lang(destination_folder_path)
#if path_to_en_US_lang is not null or empty, ask the user if they would like to carry out text analysis on the en_US.lang file
if path_to_en_US_lang:
    do_text_analysis = input("Would you like to carry out text analysis on the en_US.lang file? (y/n): ")
#if the user would like to carry out text analysis on the en_US.lang file, then call the function to carry it out
if do_text_analysis.lower() == "y":
    print(path_to_en_US_lang)
    text_analysis(path_to_en_US_lang)



    
    

