# -*- coding: utf-8 -*-
'''
    Simple Nepali stemmer
    
    Date: 04/23/2020
    
    References:
        Suffix : https://github.com/birat-bade/NepaliStemmer
        Nepali Dictionary : https://github.com/PraveshKoirala/stemmer
        Algorithm : https://github.com/sainimohit23/hindi-stemmer
'''

import re
import sys
import string
from helper import *


class NepStemmer:
    def __init__(self, dict_path=None, suffix_path=None):
        if dict_path==None:
            dict_path = "stemmer_files/dictionary.txt"
        if suffix_path==None:
            suffix_path = "stemmer_files/suffix.txt"
        self.nep_dict = nep_dictionary(dict_path)
        self.suffix_path = suffix_path
        self.suffixes = self.get_suffix()
        
        
    def get_suffix(self):        
        # Create a dictionary based on the length of suffix
        with open(self.suffix_path, 'r') as suff_file:
            suffixes = {}
            for row in suff_file.read().splitlines():
                stem_len = len(list(row))
                if stem_len not in suffixes:
                    suffixes[stem_len] = [row]
                else:
                    suffixes[stem_len] += ([row])

        return suffixes


    # Devanagari range \u0900-\u097F
    # Alphanumeric range \w
    def clean_text(self, text, chars=None):
        # puncts = string.punctuation+"—()\"#/@;:<>{}`+-=~|!?,'।॥‘’–…⁄"
        
        # Except the necessary unicode range
        puncts = "^\w\u0900-\u097F"
        
        # if text contains only punctuations
        if text in list(puncts):
            return text
        
        if chars == None:
            text = re.findall(r"[\w\u0900-\u097F]+|["+puncts+"]", text)
        else:
            text = re.findall(r"[\w\u0900-\u097F]+|[" +chars+puncts+"]", text)
        return text


    '''
        Reference: https://github.com/sainimohit23/hindi-stemmer
    '''
    def nep_stem(self, word, clean=True, chars=None):
        if clean == True:
            # Return the text with punctuation separated
            word = self.clean_text(word, chars)

        # if text cleaned, return the added the punctuation at the end
        # process only first part of cleaned_text
        punct=''
        if clean:
            ans = word[0]
            core_word = word[0]            
            if len(word) > 1:
                punct = ''.join(word[1:])

        else:
            ans = word
            core_word = word

        bl = False

        # Do not stem the word which is from
        # Nepali dictionary
        if ans in self.nep_dict:
            # Reattach the punctuation
            return ans+punct if len(word)>1 else ans

        if ans.replace('ी', 'ि') in self.nep_dict:
            return ans+punct if len(word)>1 else ans

        if ans.replace('ू', 'ु') in self.nep_dict:
            return ans+punct if len(word)>1 else ans

        if ans.replace('ं', ' ँ') in self.nep_dict:
            return ans+punct if len(word)>1 else ans

        if ans.replace('ी', 'ि').replace('ू', 'ु') in self.nep_dict:
            return ans+punct if len(word)>1 else ans

        if ans.replace('ी', 'ि').replace('ं', ' ँ') in self.nep_dict:
            return ans+punct if len(word)>1 else ans

        if ans.replace('ी', 'ि').replace('ं', ' ँ').replace('ू', 'ु') in self.nep_dict:
            return ans+punct if len(word)>1 else ans

        for w in self.nep_dict:
            if ans.replace('ी', 'ि').replace('ं', ' ँ').replace('ू', 'ु') == w.replace('ी', 'ि').replace('ं', ' ँ').replace('ू', 'ु'):
                return ans+punct if len(word)>1 else ans

        # Iteratively process the stem
        for L in 9, 8, 7, 6, 5, 4, 3, 2:
            if len(core_word) > L + 1:
                for suf in self.suffixes[L]:
                    if core_word.endswith(suf):
                        ans = core_word[:-L] + ' ' + core_word[-L:]
                        bl =True
            if bl == True:
                break

        # Might be required later for unit length suffixes
    #     if bl == True:
    #         for suf in suffixes[1]:
    #             if ans.endswith(suf):
    #                 ans = nep_stem(ans)

        # Might be required later for transformation in suffixes
    #     for suf in special_suffixes:
    #         if ans.endswith(suf):
    #             l = len(suf)
    #             ans = ans[:-l]
    #             ans += dict_special_suffixes[suf] 

        # Reattach the punctuation
        return ans+punct if len(word)>1 else ans


    # Stems the given string
    def stem(self, input_string, clean=True, chars=None):
        result = []
        # Removal of newlines and tabs
        input_string = input_string.replace('\n','')
        input_string = input_string.replace('\t','')
        for each in input_string.split():
            result.append(self.nep_stem(each, clean=True))
        return ' '.join(result)
       

