from . import dutch_words

# Define your function for calculating the difficulty of card tokens
def words_grade(words):
    # Initialize variables to store total difficulty and number of tokens
    grades = {}
    
    # Iterate over each token in the list
    for word in words:
        # Calculate the difficulty of the token (e.g., based on word length, frequency, etc.)
        if word not in grades:
            word_grade = calculate_word_grade(word)
            grades[word] = word_grade
    
    grades_list = list(grades.values())
    average_grade = sum(grades_list) / len(grades_list) 
    return average_grade, grades_list

# The ranking is standerized between [0,1]
#  0 being the most frequeny word and 1 being the least,
#  -1 means the word is not found, likely a typo or foreign word
def find_dutch_frequency_ranking(word_to_look_up):
    signs = set("?.,\"!@#$%^&*()_")
    if word_to_look_up in signs:
        return 0
    word_lower = word_to_look_up.lower()
    word_capital_first = word_lower[0].upper() + word_lower[1:]
    # It's a list of words ranked by frequency from [0, 10,000] 0 being the most frequent
    ranked_dutch_words = dutch_words.get_ranked()
    wordIndex = 0
    found = False
    for key, ranked_word in enumerate(ranked_dutch_words):
        if ranked_word == word_lower or ranked_word == word_capital_first:
            wordIndex = key
            found = True
            break
    if not found:
        return 1
    return round(wordIndex/10000, 2)

def normalize_word_length(word_length):
    max_word_length = 30

    normalized_length = word_length / max_word_length
    return normalized_length

def calculate_word_grade(word, language="nl"):
    # Don't really support languages other than dutch for the moment
    if language != "nl":
        return

    weight_for_word_frequency = 0.8
    weight_for_word_length = 0.2

    ranking_in_frequency = find_dutch_frequency_ranking(word)
    ranking_in_length = normalize_word_length(len(word))
    final_difficulty = weight_for_word_frequency * ranking_in_frequency + weight_for_word_length * ranking_in_length   
    return round(final_difficulty, 2)