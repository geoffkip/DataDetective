# Team Titans: DataDetective :mag:
This project is part of the [Code4PA Hackathon](https://www.code4pa.tech/).

## Project Overview
DataDetective aims to integrate all the economic, education, and health related data sets available on data.pa.gov. Our project is focused on visualizing multiple data sets at the same time to provide users with a way to explore the data.

### Features:
* **Measure Selector:** Select measures from across multiple data sets to plot on a time-series data visual.
* **Data Visual Recommender:** Based on the selected measures, find other data (not time-series) to display adding context to the time-series visual.
* **Ingestion Engine:** Ingest data sets into a form that can be easily visualized. Also, categorize and tag the data sets so users can easily search and explore the data sets.

### Personas:
Our application targets a few personas with the following high-level stories:

**Agency Executive:** As an Agency Executive, I want an easy way to explore the data on data.pa.gov so I can find trends that might be worth further investigation.

**Data-driven Reporter:** As a Data-driven Reporter, I want to find noteworthy insights from the data on data.pa.gov so I can find something to publish or further investigate.

**Researcher:** As a researcher, I want to access and compare data sets to support my hypotheses. The option to utilize a database with multiple data sets where I can easily compare and manipulate data which will streamline my research efforts. 

## Development Process and Methodology
DataDetective is built using ElasticSearch and Python Flask. We ingest the data sets into ElasticSearch using Python scripts. We collect the categories and tags associated with the data sets so DataDetective can suggest data sets to visualize. We split into two teams, one team to build out the interface for exploring, one team to ingest the data.

### Team Titans
#### :hammer_and_wrench: Platform Engineering
**Mission:** Build the application, support the platform on GCP
* Geoffry Kip (@gjerome1991)
* Brilzen Varghese (@x777billy)

#### :microscope: Data Science
**Mission:** Extract, transform, load, and master the data
* Marissa Bredesen (@mmbredesen)
* Edna Galindo (@Marys0l)
* Kyle McGrogan (@mcgrogan91)

#### :construction_worker_man: Overwatch
**Mission:** Maintain the flow
* Michael Ghen (@mikeghen)

### Tool Chain
* GitHub
* Google Drive
* Google Cloud Platform
* Ubuntu
* ElasticSearch
* Python
* Flask
