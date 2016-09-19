import glob
import duolingo
import os
import sys
import getpass
import datetime


def main(argv):
    print("/--------------------------------\\")
    print("|Duolingo comprehension estimator|")
    print("\--------------------------------/")
    print("Login using your duolingo credentials")
    duo_username = input("Enter your username: ")
    duo_password = getpass.getpass("Enter your password: ")
    try:
        user = duolingo.Duolingo(duo_username, password=duo_password)
    except:
        print("Error: login failed")
    else:
        language = get_requested_language(user)
        known_words = get_known_words(user, language)
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        print("Looking for files in " + path)
        files = glob.glob(path + "/*.txt")
        if files:
            print_stats(files, language, known_words)
        else:
            print("Error: no .txt files found in path")


def get_requested_language(user):
    available_languages = user.get_languages()
    language_abbreviations = user.get_languages(abbreviations=True)
    print("Available languages")
    for index, lang in enumerate(available_languages):
        print(language_abbreviations[index] + " - " + lang)
    return input("Select language: ")


def get_known_words(user, requested_language):
    vocabulary_data = user.get_vocabulary(language_abbr=requested_language)
    vocabulary = vocabulary_data['vocab_overview']
    known_words = []
    for word in vocabulary:
        word_string = word['word_string']
        known_words.append(word_string)
    return known_words


def print_stats(files, language, known_words):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    logfilename = timestamp + "-" + language + ".txt"
    logfile = open(logfilename, "w")
    for f in files:
        logfile.write("Stats for " + os.path.split(f)[1] + "\n")
        print("Stats for " + os.path.split(f)[1])
        text = open(f, "r")
        stats = get_textstats(text, known_words)
        logfile.write("\t Total Words: " + str(stats[0]) + "\n")
        print("\t Total Words: " + str(stats[0]))
        logfile.write("\t Known Words: " + str(stats[1]) + "\n")
        print("\t Known Words: " + str(stats[1]))
        logfile.write("\t Ratio: " + str('{:.1%}'.format(stats[2])) + "\n")
        print("\t Ratio: " + str('{:.1%}'.format(stats[2])))
        text.close()
    logfile.close()
    print("Logfile written: " + logfilename)


def get_textstats(text, known_words):
    total_words = 0
    matching_words = 0
    for line in text:
        for word in line.split():
            total_words += 1
            if word:
                if word in known_words:
                    matching_words += 1
    ratio = float(matching_words / total_words)
    return(total_words, matching_words, ratio)


if __name__ == "__main__":
    main(sys.argv)
