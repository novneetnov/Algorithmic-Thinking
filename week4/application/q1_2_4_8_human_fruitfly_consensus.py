import proj4_solution as student
import alg_application4_provided as provided
import random
import math
import time
import matplotlib.pyplot as plt


def local_alignment_eyeless_protein():
    """
    Question: 1
    """
    human_eyeless_seq = provided.read_protein(provided.HUMAN_EYELESS_URL)
    fruitfly_eyeless_seq = provided.read_protein(provided.FRUITFLY_EYELESS_URL)
    scoring_matrix = provided.read_scoring_matrix(provided.PAM50_URL)
    alignment_matrix = student.compute_alignment_matrix(human_eyeless_seq, fruitfly_eyeless_seq, scoring_matrix, False)
    local_alignment = student.compute_local_alignment(human_eyeless_seq, fruitfly_eyeless_seq, scoring_matrix, alignment_matrix)
    return local_alignment

#print local_alignment_eyeless_protein()


def global_alignment_consensus():
    """
    Question: 2
    """
    ans_similar = []
    local_alignments = local_alignment_eyeless_protein()
    consensus_seq = provided.read_protein(provided.CONSENSUS_PAX_URL)
    scoring_matrix = provided.read_scoring_matrix(provided.PAM50_URL)
    for idx in range(1, 3):
        seq_x = local_alignments[idx]
        seq_x = seq_x.replace("-", "")
        alignment_matrix = student.compute_alignment_matrix(seq_x, consensus_seq, scoring_matrix, True)
        global_alignment = student.compute_global_alignment(seq_x, consensus_seq, scoring_matrix, alignment_matrix)
        similar_count = 0
        for letter1, letter2 in zip(global_alignment[1], global_alignment[2]):
            if letter1 == letter2:
                similar_count += 1
        ans_similar.append(float(similar_count * 100) / len(global_alignment[1]))
    return ans_similar

#print global_alignment_consensus()


def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Question: 4: Compute null distribution
    """
    scoring_distribution = {}
    for _ in range(num_trials):
        rand_y = list(seq_y)
        random.shuffle(rand_y)
        rand_y = "".join(rand_y)
        print _
        alignment_matrix = student.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        max_score = max(map(max, alignment_matrix))
        if scoring_distribution.has_key(max_score):
            scoring_distribution[max_score] += 1
        else:
            scoring_distribution[max_score] = 1
    return scoring_distribution


def bar_plot(scoring_distribution, num_trials):
    """
    Question: 4: Bar  plot
    """
    x_vals = []
    y_vals = []
    for entry in scoring_distribution:
        x_vals.append(entry)
        y_vals.append(float(scoring_distribution[entry]) / num_trials)
    plt.bar(x_vals, y_vals)
    plt.xlabel("Maximum score for Local Alignment")
    plt.ylabel("Fraction of total trials corresponding to each score")
    plt.grid = True
    plt.title("Distribution of Local Alignment Scores of Human and Permutations of Fruitfly")
    plt.show()


def compute_stats(distribution, num_trials):
    """
    Returns the mean ans std_dev of the distribution.
    """
    total = 0
    for key in distribution:
        total += key * distribution[key]
    mean = float(total) / num_trials
    total = 0
    for key in distribution:
        total += (float(key - mean) ** 2.0) * distribution[key]
    std_dev = math.sqrt(float(total) / num_trials)
    return mean, std_dev


def run_ques_4():
    """
    Question: 4 & 5
    """
    seq_x = provided.read_protein(provided.HUMAN_EYELESS_URL)
    seq_y = provided.read_protein(provided.FRUITFLY_EYELESS_URL)
    scoring_matrix = provided.read_scoring_matrix(provided.PAM50_URL)
    num_trials = 1000
    scoring_distribution = generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials)
    mean, std_dev = compute_stats(scoring_distribution, num_trials)
    print mean, ",", std_dev
    z_score = float(local_alignment_eyeless_protein()[0] - mean) / std_dev
    print z_score
    bar_plot(scoring_distribution, num_trials)

#run_ques_4()


def compute_edit_distance(word1, word2, scoring_matrix):
    """
    Question 7
    :return: The edit_distance between word1 and word2
    """
    alignment_matrix = student.compute_alignment_matrix(word1, word2, scoring_matrix, True)
    global_score = alignment_matrix[len(word1)][len(word2)]
    edit_distance = len(word1) + len(word2) - global_score
    return edit_distance

from string import lowercase


def check_spelling(checked_word, dist, word_list):
    """
    Helper function for Question: 8
    :param checked_word: The target word
    :param dist: The given edit_distance
    :param word_list: The given list of words
    :return: A set of all words that are within the given edit_distance from the checked_word.
    """
    outcome_set = set()
    scoring_matrix = student.build_scoring_matrix(lowercase, 2, 1, 0)
    len_checked_word = len(checked_word)
    for word in word_list:
        if abs(len(word) - len_checked_word <= dist):
            edit_distance = compute_edit_distance(word, checked_word, scoring_matrix)
            if edit_distance <= dist:
                outcome_set.add(word)
    return outcome_set


def run_ques_8():
    """
    Question: 8
    """
    word_list = provided.read_words(provided.WORD_LIST_URL)
    checked_word1 = "humble"
    time1 = time.time()
    similar_words1 = check_spelling(checked_word1, 1, set(word_list))
    time2 = time.time()
    print similar_words1
    print time2 - time1

    checked_word2 = "firefly"
    time3 = time.time()
    similar_words2 = check_spelling(checked_word2, 2, set(word_list))
    time4 = time.time()
    print similar_words2
    print time4 - time3

run_ques_8()


def compute_edit_dist_one(word):
    """
    :param word: The input word
    :return: A set of words with edit_distance one from the given inout word
    """
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces = [a + c + b[1:] for a, b in splits for c in lowercase if b]
    inserts = [a + c + b for a, b in splits for c in lowercase]
    return set(deletes + replaces + inserts)


def check_spelling_fast(checked_word, dist, dictionary_set):
    """
    :param checked_word: The target word
    :param dist: The given edit_distance
    :param dictionary_set: The given list of words
    :return: A set of all words that are within the given edit_distance from the checked_word.
    """
    outcome_set = set()
    edit_dist_dict = {0: set([checked_word])}
    for idx in range(1, dist + 1):
        set_of_dist_words = set()
        prev_dist_words = edit_dist_dict[idx - 1]
        for word in prev_dist_words:
            close_words_set = compute_edit_dist_one(word)
            if idx == dist:
                close_words_set = close_words_set.intersection(dictionary_set)
            set_of_dist_words = set_of_dist_words.union(close_words_set)
        edit_dist_dict[idx] = set_of_dist_words
    for edit_dist_key in edit_dist_dict:
        words_set = edit_dist_dict[edit_dist_key]
        for word in words_set:
            if word in dictionary_set:
                outcome_set.add(word)
    return outcome_set


def run_ques_9():
    """
    Question: 9
    """
    word_list = provided.read_words(provided.WORD_LIST_URL)
    checked_word1 = "humble"
    time1 = time.time()
    similar_words1 = check_spelling_fast(checked_word1, 1, set(word_list))
    time2 = time.time()
    print similar_words1
    print time2 - time1

    checked_word2 = "firefly"
    time3 = time.time()
    similar_words2 = check_spelling_fast(checked_word2, 2, set(word_list))
    time4 = time.time()
    print similar_words2
    print time4 - time3

run_ques_9()