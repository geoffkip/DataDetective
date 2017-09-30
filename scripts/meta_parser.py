import urllib2
import json


DATA_FILE_PATH = 'data.pa.gov.csv'

def escape(string):
    return '"%s"' % string

def extract():
    """
    Extracts data from a URL. Returns the data extracted as a dictionary.
    """
    URL = 'http://data.pa.gov/api/catalog/v1?domains=data.pa.gov&search_context=data.pa.gov'


    # Get JSON data from the URL
    response        = urllib2.urlopen(URL)
    extracted_data  = json.load(response)

    return extracted_data

def get(data):
    records = []
    for dataset in data["results"]:
        #print (resource.keys())
        resource = dataset["resource"]
        classification = dataset["classification"]
        name = resource["name"]
        id_data = resource["id"]
        categories = classification["categories"]
        tags = classification["domain_tags"]
        link = dataset["link"]

        str_c = ','.join(categories)
        str_t = ','.join(tags)

        record = (name,id_data, link, str_c, str_t)

        records.append(record)

    return records

def load(records):
        record_counter = 0
        with open(DATA_FILE_PATH, 'w') as data_file:
            for record in records:
            # Write 1 record per line
                data_file.write(','.join(map(escape, record)))
                data_file.write('\n')
                record_counter += 1


pa_data = extract()
pa_records = get(pa_data)
written_records = load(pa_records)
