
import json

definitions_path = 'data/translator_definitions.json'
definitions = None
with open(definitions_path) as data_file:
    definitions = json.load(data_file)

for definition in definitions:
    # print "Runner"
    # print json.dumps(definition)
    module = __import__(definition['translation_file'])
    class_ = getattr(module, definition['translation_class'])
    translator = class_(definition=definition)

    data = translator.extract()
    transformed = translator.transform(data)

    print json.dumps(transformed)

