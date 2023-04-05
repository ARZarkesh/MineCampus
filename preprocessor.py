from pandas import DataFrame
import string
import nltk
from bs4 import BeautifulSoup
from spellchecker import SpellChecker
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

class Preprocessor:
    def __init__(self, df: DataFrame):
        self.data_frame = df
        self.data_frame.dropna(inplace=True)
        self.important_columns = [
            'country_name', 
            'university_name', 
            'program_name', 
            'program_type', 
            'language', 
            'tution_1_type', 
            'tution_2_type', 
            'structure', 
            'academic_req', 
            'facts', 
            'city'
        ]
        self.lowercase()
        self.remove_punctuations()
        self.remove_stopwords()
        self.remove_html()
        # self.correction_words()
        self.collect_words()
        
    def lowercase(self):
        for column in self.important_columns:
            self.data_frame[column] = self.data_frame[column].str.lower()
     
       
    def _remove_puncs(self, text, puncs):
        return text.translate(str.maketrans('', '', puncs))

    def remove_punctuations(self):
        """this function removes !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ from strings"""
        puncs = string.punctuation
        
        for column in self.important_columns:
            self.data_frame[column] = self.data_frame[column].apply(lambda text: self._remove_puncs(text, puncs)) 

    def remove_stopwords(self):
        nltk.download('stopwords')
        stopwords = set(nltk.corpus.stopwords.words('english'))
        for column in self.important_columns:
            self.data_frame[column] = self.data_frame[column].apply(
                lambda text: " ".join([word for word in str(text).split() if word not in stopwords])
            )
            
    def remove_html(self):
        self.data_frame['academic_req'] = self.data_frame['academic_req'].apply(
            lambda text: BeautifulSoup(text, 'lxml').text
        )
            
    # def _correct_spellings(self, text: str):
    #     spell = SpellChecker()
    #     corrected_text = []
    #     misspelled_words = spell.unknown(text.split())
        
    #     for word in text.split():
    #         if word in misspelled_words and spell.correction(word) is not None:
    #             corrected_text.append(spell.correction(word))
    #         else:
    #             corrected_text.append(word)
                
    #     return " ".join(corrected_text)
    
    # def correction_words(self):
    #     for column in self.important_columns:
    #         self.data_frame[column] = self.data_frame[column].apply(
    #             lambda text: self._correct_spellings(text)
    #         )
    
    def collect_words(self):
        sentences = []
        for row in range(self.data_frame.shape[0]):
            words = []
            for column in self.important_columns:
                for text in self.data_frame.iloc[row][column].split():
                    words.append(text)

            sentences.append(" ".join(set(words)))
            # self.generate_wordcloud(" ".join(set(words))) 
            
    
        self.data_frame['extracted_keywords'] = sentences         

    def generate_wordcloud(self, words):
        wordcloud = WordCloud(
                width=800, 
                height=800, 
                background_color='white', 
                stopwords=set(STOPWORDS), 
                min_font_size=10
            ).generate(words)
            
        plt.figure(figsize = (8, 8), facecolor = None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad = 0)
        
        plt.show()
        
    def get_specific_column(self, column: str):
        return self.data_frame[column].tolist()
        