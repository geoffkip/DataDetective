from parse_base import Translator
import json

class TranslatorTest(Translator):
    def transformDataValue(self, column, value):
        if column == 'date':
            return value[1] + ' ' + value[0]
        return super(TranslatorTest, self).transformDataValue(column, value)