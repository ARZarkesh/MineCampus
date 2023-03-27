from pandas import DataFrame
import string
import nltk

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
            
