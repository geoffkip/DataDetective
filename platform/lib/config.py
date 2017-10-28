import random
import datetime,time

COUNTIES_FIPS = [
"Adams",
"Armstrong",
"Beaver",
"Bedford",
"Statewide",
"Alleghany",
"Northampton",
"Luzerne",
"Lancaster",
"Philadelphia",
"Washington",
"Bradford",
"Dauphin",
"Snyder",
"Deleware",
"Bucks",
"Montgomery",
"Lackawanna",
"Schuylkill",
"Mifflin",
"Franklin",
"Union",
"York",
"Lycoming",
"Centre",
"Blair",
"Fayette",
"Mercer",
"Pike",
"Chester",
"Monroe",
"Carbon",
"Indiana",
"Huntingdon",
"Greene",
"Forest",
"Wayne",
"Clearfield",
"Somerset",
"Crawford",
"Norhumberland",
"Berks",
"Tioga",
"Columbia",
"Butler",
"Susquehanna",
"Cameron",
"Warren",
"Venango",
"Lebanon",
"Lawrence",
"Cambria",
"Montour",
"Juniata",
"Jefferson",
"Clinton",
"McKean",
"Potter"
]
MEASURES_LIST= [
    {"name": "corrections_population"},
    {"name": "jobs_pledged_to_be_created"},
    {"name": "jobs_pledged_to_be_retained"},
    {"name": "corrections_population"},
    {"name": "ma_individuals"},
    {"name": "ma_children"},
    {"name": "total_jobs"}
]

def generate_series(measure):
    random.seed(abs(hash(measure)))
    return {
        "data": list(map((lambda c: [c,random.randint(0,100)]), COUNTIES)),
        "name": measure
    }

def generate_timeseries(measure):
    random.seed(abs(hash(measure)))
    return {
        "name": measure,
        "data": [[time.mktime(datetime.datetime(2017,1,1).utctimetuple())*1000,random.randint(0,100)],
        [time.mktime(datetime.datetime(2017,2,1).utctimetuple())*1000,random.randint(0,100)],
        [time.mktime(datetime.datetime(2017,3,1).utctimetuple())*1000,random.randint(0,100)],
        [time.mktime(datetime.datetime(2017,4,1).utctimetuple())*1000,random.randint(0,100)],
        [time.mktime(datetime.datetime(2017,5,1).utctimetuple())*1000,random.randint(0,100)],
        [time.mktime(datetime.datetime(2017,6,1).utctimetuple())*1000,random.randint(0,100)],
        [time.mktime(datetime.datetime(2017,7,1).utctimetuple())*1000,random.randint(0,100)],
        [time.mktime(datetime.datetime(2017,8,1).utctimetuple())*1000,random.randint(0,100)],
        [time.mktime(datetime.datetime(2017,9,1).utctimetuple())*1000,random.randint(0,100)],
        [time.mktime(datetime.datetime(2017,10,1).utctimetuple())*1000,random.randint(0,100)],
        [time.mktime(datetime.datetime(2017,11,1).utctimetuple())*1000,random.randint(0,100)],
        [time.mktime(datetime.datetime(2017,12,1).utctimetuple())*1000,random.randint(0,100)]]
    }
