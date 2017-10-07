from parse_base import Translator
import json

class TranslatorTest(Translator):
    data_url = 'http://data.pa.gov/resource/sshd-za9g.json'
    # def transformDataValue(self, column, value):
    #     if column == 'date':
    #         return 'No date for you'
    #     return super(TranslatorTest, self).transformDataValue(column, value)


translator = TranslatorTest('/Users/kmcgrogan/Programming/DataDetective/data/test_definition.json')

data = translator.extract()
transformed = translator.transform(data)

print json.dumps(transformed)