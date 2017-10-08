import csv
import json

f = open( '/Users/edna/DataDetective/data/Hospitalization.csv', 'rU' )

reader = csv.DictReader(f)

out = json.dumps( [ row for row in reader ] )
print "JSON parsed!"

f = open( '/Users/edna/DataDetective/data/hospitalizations.json', 'w')
f.write(out)
print "JSON saved!"
