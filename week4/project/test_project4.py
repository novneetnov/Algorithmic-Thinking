"""
Test the 4 functions of proj4_solution.
Implement 4 corresponding test functions.
"""
import proj4_solution
import poc_simpletest


def test_build_scoring_matrix():
    """
    Test the running of build_scoring_matrix function
    """
    suite = poc_simpletest.TestSuite()

    alphabet = set("abcd")
    scoring_matrix = proj4_solution.build_scoring_matrix(alphabet, 10, 4, -4)
    print scoring_matrix
    suite.run_test(scoring_matrix['a']['a'], 10, 'Something is wrong')

    scoring_matrix = proj4_solution.build_scoring_matrix(set(['A', 'C', 'T', 'G']), 6, 2, -4)
    print scoring_matrix
    suite.run_test(scoring_matrix['A']['A'], 6, 'Something is wrong')

    suite.report_results()


def test_compute_alignment_matrix():
    """
    Test the function compute_alignment_matrix function
    """
    suite = poc_simpletest.TestSuite()
    scoring_matrix = proj4_solution.build_scoring_matrix(set(['A', 'C', 'T', 'G']), 10, 4, -6)
    global_alignment_matrix = proj4_solution.compute_alignment_matrix('AA', 'TAAT', scoring_matrix, False)
    print global_alignment_matrix
    suite.run_test(global_alignment_matrix[1][2], 4,"Error Found")

    suite.report_results()


def test_compute_global_alignment():
    """
    Test the function compute_global_alignment function
    """
    suite = poc_simpletest.TestSuite()
    scoring_matrix = proj4_solution.build_scoring_matrix(set(['A', 'C', 'T', 'G']), 10, 4, -6)
    alignment_matrix = proj4_solution.compute_alignment_matrix('AA', 'TAAT', scoring_matrix, True)
    global_alignment_sequence = proj4_solution.compute_global_alignment('AA', 'TAAT', scoring_matrix, alignment_matrix)
    print global_alignment_sequence
    suite.run_test(global_alignment_sequence, (8, '-AA-', 'TAAT'),"Error Found")

    global_alignment_sequence = proj4_solution.compute_global_alignment('ACTACT', 'AGCTA',
                                                                        {
                                                                            'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1},
                                                                            'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1},
                                                                            '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0},
                                                                            'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1},
                                                                            'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}
                                                                        },
                                                                        [
                                                                            [0, 0, 0, 0, 0, 0],
                                                                            [0, 2, 2, 2, 2, 2],
                                                                            [0, 2, 3, 4, 4, 4],
                                                                            [0, 2, 3, 4, 6, 6],
                                                                            [0, 2, 3, 4, 6, 8],
                                                                            [0, 2, 3, 5, 6, 8],
                                                                            [0, 2, 3, 5, 7, 8]])
    print global_alignment_sequence
    suite.run_test(global_alignment_sequence, (8, 'A-CTACT', 'AGCTA--'),"Error Found")

    global_alignment_sequence = proj4_solution.compute_global_alignment('ACTACT', 'GGACTGCTTCTGG',
                                                                        {
                                                                            'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1},
                                                                            'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1},
                                                                            '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0},
                                                                            'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1},
                                                                            'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}
                                                                        },
                                                                        [
                                                                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                            [0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                                                                            [0, 1, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                                                            [0, 1, 2, 3, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6],
                                                                            [0, 1, 2, 4, 4, 6, 7, 7, 7, 7, 7, 7, 7, 7],
                                                                            [0, 1, 2, 4, 6, 6, 7, 9, 9, 9, 9, 9, 9, 9],
                                                                            [0, 1, 2, 4, 6, 8, 8, 9, 11, 11, 11, 11, 11, 11]])
    print global_alignment_sequence
    suite.run_test(global_alignment_sequence, (11, '--A---CTACT--', 'GGACTGCTTCTGG'),"Error Found")

    suite.report_results()


def test_compute_local_alignment():
    """
    Test the function compute_global_alignment function
    """
    suite = poc_simpletest.TestSuite()
    scoring_matrix = proj4_solution.build_scoring_matrix(set(['A', 'C', 'T', 'G']), 10, 4, -6)
    alignment_matrix = proj4_solution.compute_alignment_matrix('AA', 'TAAT', scoring_matrix, False)
    local_alignment_sequence = proj4_solution.compute_local_alignment('AA', 'TAAT', scoring_matrix, alignment_matrix)
    print local_alignment_sequence
    suite.run_test(local_alignment_sequence, (20, 'AA', 'AA'),"Error Found")

    scoring_matrix = proj4_solution.build_scoring_matrix(set(['A', 'C', 'T', 'G']), 10, 2, -4)
    alignment_matrix = proj4_solution.compute_alignment_matrix('---AC-C--', 'TTTACACGG', scoring_matrix, False)
    local_alignment_sequence = proj4_solution.compute_local_alignment('---AC-C--', 'TTTACACGG', scoring_matrix, alignment_matrix)
    print local_alignment_sequence
    suite.run_test(local_alignment_sequence, (26, 'AC-C', 'ACAC'),"Error Found")

    local_alignment_sequence = proj4_solution.compute_local_alignment('A', 'A',
                                                              {
                                                                  'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
                                                                  'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
                                                                  '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
                                                                  'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}
                                                              },
                                                              [[0, 0], [0, 6]])
    print local_alignment_sequence
    suite.run_test(local_alignment_sequence, (6, 'A', 'A'),"Error Found")

    suite.report_results()


def run_example():
    #test_build_scoring_matrix()
    #test_compute_alignment_matrix()
    #test_compute_global_alignment()
    test_compute_local_alignment()

run_example()
