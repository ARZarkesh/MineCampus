from pandas import DataFrame

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
        
    def lowercase(self):
        for column in self.important_columns:
            for data in self.data_frame[column]:
                data = data.lower()    