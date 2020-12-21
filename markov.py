'''
MPCS 51042 S'20: Markov models and hash tables

Cole Bryant
'''
from hash_table import Hashtable
import math

HASH_CELLS = 57

# Recommended load factor and growth factor for the assignment
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:
    """Class which represents a Markov Model (learning algorithm) used to
    asses the likelihood that a speaker uttered a given text."""

    def __init__(self, text_string, k, state):
        self._text = text_string
        self._k = k
        self._state = state
        self._unique_chars = []
        self._model = self.populate_model()

    def populate_model(self):
        """Method which populates the hashtable (or dictionary, depending on
        state) for the model.
        No inputs.
        Outputs: Hashtable or dictionary
        """
        if self._state == 1:
            model = Hashtable(HASH_CELLS, 0, 0.5, 2)
        else:
            model = dict()
        for i in range(len(self._text)):
            k_string = ''
            k_plus_one_string = ''
            # Collect unique characters in text
            if self._text[i] not in self._unique_chars:
                self._unique_chars.append(self._text[i])
            # Loop through and build k and k + 1 strings
            for j in range(self._k + 1):
                if i + j >= len(self._text):
                    index = i + j - len(self._text)
                else:
                    index = i + j

                if j < self._k:
                    k_string += self._text[index]
                k_plus_one_string += self._text[index]
            if k_string in model:
                model[k_string] += 1
            else:
                model[k_string] = 1

            if k_plus_one_string in model:
                model[k_plus_one_string] += 1
            else:
                model[k_plus_one_string] = 1
        return model

    def log_probability(self, unknown_speech):
        """Method which takes in a new string (an unknown speech) and
        calculates and returns the log probability that the current modeled
        speaker uttered it.
        Inputs: String (unknown_speech)
        Outputs: Float
        """
        total = 0
        S = len(self._unique_chars)

        for i in range(len(unknown_speech)):
            k_string = ''
            k_plus_one_string = ''
            # Loop through and build k and k + 1 strings
            for j in range(self._k + 1):
                if i + j >= len(unknown_speech):
                    index = i + j - len(unknown_speech)
                else:
                    index = i + j

                if j < self._k:
                    k_string += unknown_speech[index]
                k_plus_one_string += unknown_speech[index]

            if k_plus_one_string in self._model:
                M = self._model[k_plus_one_string]
            else:
                M = 0
            if k_string in self._model:
                N = self._model[k_string]
            else:
                N = 0

            total += math.log((M + 1) / (N + S))

        return total


def identify_speaker(speaker_a, speaker_b, unknown_speech, order, state):
    """Builds markov models for two strings (speakers) given, and calculates
    normalized log probabilities that the two speakers uttered the third
    string. Returns a tuple of the two probabilites, and conclusion string
    A or B.
    Inputs: String (speaker_a), string (speaker_b), string (unknown_speech),
    integer (order), integer (state)
    Outputs: Tuple
    """
    speaker_a_model = Markov(speaker_a, order, state)
    speaker_b_model = Markov(speaker_b, order, state)

    string_length = len(unknown_speech)

    prob_a = speaker_a_model.log_probability(unknown_speech) / string_length
    prob_b = speaker_b_model.log_probability(unknown_speech) / string_length

    return prob_a, prob_b, 'A' if prob_a > prob_b else 'B'


