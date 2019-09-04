from .exceptions import *
from random import choice


class GuessAttempt(object):
    def __init__(self, letter, hit=False, miss=False):
        self.letter = letter
        self.hit = hit
        self.miss = miss
        if self.hit and self.miss:
            raise InvalidGuessAttempt(
            "Cannot be a hit and a miss at the same time.")
    
    def is_hit(self):
        if self.hit and not self.miss:
            return True
        return False
    
    def is_miss(self):
        if self.miss and not self.hit:
            return True
        return False


class GuessWord(object):
    def __init__(self, answer):
        self.answer = answer
        self.masked = "*" * len(answer)
        if not answer:
            raise InvalidWordException(
            "You cannot have an empty guess word.")
            
    
    def perform_attempt(self, letter):
        if len(letter) != 1:
            raise InvalidGuessedLetterException(
                "Sorry, your can only guess ONE letter at a time.")
        
        if letter.lower() not in self.answer.lower():
            return GuessAttempt(letter, miss=True)
            
        new_word = ''
        for ans_let, mask_let in zip(self.answer.lower(), self.masked):
            if letter.lower() == ans_let.lower():
                new_word += ans_let
            else:
                new_word += mask_let
        self.masked = new_word
        return GuessAttempt(letter, hit=True)
            

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=WORD_LIST, number_of_guesses=5): 
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(word_list))
    
    def is_won(self):
        return self.word.masked == self.word.answer.lower()
    
    def is_lost(self):
        return self.remaining_misses == 0
    
    def is_finished(self):
        return self.is_won() or self.is_lost()
    
    def guess(self, letter):
        if letter.lower() in self.previous_guesses:
            raise InvalidGuessedLetterException(
                "You already guessed that letter.")
        if self.is_finished():
            raise GameFinishedException(
                "You already finished the game.")
        
        self.previous_guesses.append(letter.lower())
        
        attempt = self.word.perform_attempt(letter.lower())
        if attempt.is_miss():
            self.remaining_misses -= 1
        if self.is_won():
            raise GameWonException("You won!")
        if self.is_lost():
            raise GameLostException("Sorry, you lost.")
        return attempt
    

    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException(
                "You need to have atleast a word to choose from.")
        return choice(word_list)