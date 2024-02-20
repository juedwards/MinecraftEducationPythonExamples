# Title: Language Change for mcworld files
# Description: This script is used to change the language of a mcworld file to all the languages minecraft education supports
# Author: Justin Edwards
# Last Updated: 2020-07-29
# Version: 0.1

#import the chatGPT library
import openai
#import the os library
import os
#import the zipfile library
import zipfile

#create a function that translates text to a different language
def translate_text(text, language):
    #set the openai api key, get key from openai_key.txt
    with open("openai_key.txt", "r") as openai_key:
        openai.api_key = openai_key.read()
    #set the prompt
    prompt = "Translate the following English text to " + language + ":\n\n" + text
    #set the engine
    engine = "davinci"
    #set the max tokens
    max_tokens = 100
    #set the temperature
    temperature = 0.5
    #set the top p
    top_p = 1
    #set the frequency penalty
    frequency_penalty = 0
    #set the presence penalty
    presence_penalty = 0
    #set the stop sequence
    stop = "\n"
    #set the response
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop
    )
    # show the user the original text and the translated text
    print("Original Text: " + text)
    print("Translated Text: " + response.choices[0].text.strip())
    #return the response
    return response.choices[0].text.strip()

#create a function that changes a mcworld file to a zip file by changing the extension
def mcworld_to_zip(mcworld_file):
    #split the file name and the extension
    file_name, file_extension = os.path.splitext(mcworld_file)
    #check if the file extension is mcworld
    if file_extension == ".mcworld":
        #change the file extension to .zip
        new_file = file_name + ".zip"
        #rename the file
        os.rename(mcworld_file, new_file)
        return new_file
    else:
        return mcworld_file
    
#create a function that checks to see if .lang file exists within the zip file located in teh resources > text folder
def lang_file_exists(zip_file, language):
    #open the zip file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        #check if the file exists
        if "resources/texts/en_US.lang" in zip_ref.namelist():
            # extract the contents of the file into a list
            file_list = zip_ref.namelist()
            # itterate through the list line by line
            for file in file_list:
                # if the line has an '"" sign then translate the text to the langague in variable 'language'  after the = sign,
                # but ignore super script symbols and the single digit number after them
                # also ignore % symbols and the number directly after them.
                # replace the line with the new translated line
                if file.endswith('.lang'):
                    with zip_ref.open(file) as lang_file:
                        lang_file = lang_file.read().decode('utf-8')
                        lang_file = lang_file.splitlines()
                        new_lang_file = []
                        for line in lang_file:
                            if "=" in line:
                                line = line.split("=")
                                if line[1] != "":
                                    line[1] = line[1].replace("§0", "").replace("§1", "").replace("§2", "").replace("§3", "").replace("§4", "").replace("§5", "").replace("§6", "").replace("§7", "").replace("§8", "").replace("§9", "").replace("§a", "").replace("§b", "").replace("§c", "").replace("§d", "").replace("§e", "").replace("§f", "").replace("§l", "").replace("§m", "").replace("§n", "").replace("§o", "").replace("§r", "").replace("%1", "").replace("%2", "").replace("%3", "").replace("%4", "").replace("%5", "").replace("%6", "").replace("%7", "").replace("%8", "").replace("%9", "").replace("%0", "")
                                    line[1] = translate_text(line[1], language)
                                    line = "=".join(line)
                            new_lang_file.append(line)
                        new_lang_file = "\n".join(new_lang_file)
                        with open("temp_lang_file.lang", "w") as temp_lang_file:
                            temp_lang_file.write(new_lang_file)
                        zip_ref.write("temp_lang_file.lang", file)
                        os.remove("temp_lang_file.lang")
                        return True
                else:
                    return False

# main function
def main():
    # ask user for the mcworld file location
    mcworld_file = input("Enter the mcworld file location: ")
    # ask teh user to select from a numbered list of languages
    print("Select a language from the list below:")
    print("1. English (US)")
    print("2. English (UK)")
    print("3. Spanish (Spain)")
    print("4. Spanish (Mexico)")
    print("5. French (France)")
    print("6. French (Canada)")

    # ask the user to select a language
    language = input("Enter the number of the language you would like to translate to: ")
    # check to see if the language is valid
    if language == "1":
        language = "en_US"
    elif language == "2":
        language = "en_GB"
    elif language == "3":
        language = "es_ES"
    elif language == "4":
        language = "es_MX"
    elif language == "5":
        language = "fr_FR"
    elif language == "6":
        language = "fr_CA"
    else:
        print("Invalid language")
        return
    
    # check to see if the mcworld file exists
    if not os.path.exists(mcworld_file):
        print("File does not exist")
        return

    #change the mcworld file to a zip file
    zip_file = mcworld_to_zip(mcworld_file)
    
                
# run the main function
main()