# DataDetective: Platform
To set up elasticsearch on the virtual machine instance(vm) I first installed Java Development Kit (JDK) 8 since elasticsearch needs this dependency to run.
The article I used can be found here -->https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04
To install run:
```
sudo apt-get install oracle-java8-installer
```

After installing Java JDK 8 or higher then you can install elasticsearch.
To install elastic search I followed the documentation here -->https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html
on the elastic search website.
To install elastic search I ran:
```
sudo apt-get update && sudo apt-get install elasticsearch.
```

Make sure that the vm you are running has enough memory to run the elasticsearch webserver (at least 2GB ram).

To start the elasticsearch server run:
```
sudo elasticsearch start
```


To check that elasticsearch is running run:
```
service elasticsearch status
```
