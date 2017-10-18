# DataDetective: Platform

## Setting up Google cloud virtual machine(VM)
A virtual machine was set up using Google's compute engine. An instance with elasticsearch pre-installed was used from Bitnami --> https://console.cloud.google.com/launcher/details/bitnami-launchpad/elasticsearch?project=boreal-quarter-181516. It was provisioned with 2 GB ram.


## Setting up elasticsearch db
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

To start the elasticsearch server run these commands as the root user:
```
# Become root user
sudo -s
# Start service
sudo elasticsearch start
```


To check that elasticsearch is running run:
```
service elasticsearch status
```

## Setting up flask app

Suggested [these instructions](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps) to set up Flask on Ubuntu.

## Install cURL on Ubuntu


To install cURL by using the apt-get install command, perform the following steps:

1.Enter the following command to download the package lists from the repositories and update them:
```
sudo apt-get update
```
2.Enter the following command to install cURL:
```
sudo apt-get install curl
```
3.To verify that cURL is running correctly, enter this command:
```
curl --version
```
A message that is similar to the following is displayed:

```
curl 7.29.0 (x86_64-redhat-linux-gnu) libcurl/7.29.0 NSS/3.15.4 zlib/1.2.7 libidn/1.28 libssh2/1.4.3
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp scp sftp smtp smtps telnet tftp
Features: AsynchDNS GSS-Negotiate IDN IPv6 Largefile NTLM NTLM_WB SSL libz
```

## Flask Example for handling Requests

```
@app.route('/users/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
        """return the information for <user_id>"""
        .
        .
        .
    if request.method == 'POST':
        """modify/update the information for <user_id>"""
        # you can use <user_id>, which is a str but could
        # changed to be int or whatever you want, along
        # with your lxml knowledge to make the required
        # changes
        data = request.form # a multidict containing POST data
        .
        .
        .
    if request.method == 'DELETE':
        """delete user with ID <user_id>"""
        .
        .
        .
else:
    # POST Error 405 Method Not Allowed
    .
    .
    .
```    
## Python Flask jQuery AJAX POST
[Link to resource](http://codehandbook.org/python-flask-jquery-ajax-post/)

## Postgresql Database Setup
Postgresql 9.6 was used to store the data points that will be used for the front-end of the app. A google cloud SQL instance of Postgresql was provisioned with 10GB of memory. Parsed json files are then loaded into the Database by connecting to it using Python and inserting them into the database using an API in Python to do so.
