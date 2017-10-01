# DataDetective: Data Science Scripts

## Flow
```
Catalog URL -> Data URL -> Raw JSON Data -> DataPoints -> Document -> ElasticSearch
      \                                               /
       \                                             /
        ---------->  Categories and Tags   ----------       
```               
## Sample Input/Output Data
**Input**
```
[{
    "countyname":"Luzerne",
    "jobs_pledged_to_be_created":"0",
    "jobs_pledged_to_be_retained":"33",
    "month":"July",
    "total_jobs":"33",
    "year":"2016"
}, ...]
```
**Output**
```
{
  "id": "d5pf-ti7w",
  "name": "All Jobs January 2015 To October 2016 Community and Economic Development"},
  "categories": ["economy", "social services"],
  "tags": ["community", "dced", "jobs", "job", "economic"],
  "data": [{
      "county": "Luzerne",
      "date": "2016-07-01",
      "jobs_pledged_to_be_created": 0,
      "jobs_pledged_to_be_retained": 33,
      "total_jobs": 33
    },
    ..
  ]
}
```
