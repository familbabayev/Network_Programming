# Client-Server based TCP web scraper console application

## Scenario
You as a software developer must create the client-server-based console app “web_scraper”. With the next abilities:

**Get statistical data:**
* Calculate the number of pictures in the webpage
* Calculate the number of the leaf paragraphs in the webpage

**Task**:
Create console-based app with two roles server and the client. The server must be started and wait the
request from the client. Server must produce the web scraping of the webpage to get two parameters:
the number of pictures and the number of the leaf paragraphs. The leaf paragraphs in HTML document
represents only the last paragraphs in the nested paragraph structures.

The client must send the request to the server to get the proper answer. The client has options page (-p) 
to get the statistical data. All the cacluation must be done on the server side

## Installation
```
git clone https://github.com/familbabayev/Network_Programming/tree/master/Lab3(Web_scraper)
```

Install the packages in the requirements.txt

## Usage
The default value(1060) for port number is assigned by the program, so if you want you can omit it.

For server:
```
python3 web_scraper.py server "" [-PORT]
```
Here "" represent 0.0.0.0 and means server can accept connections from all interfaces.

For client:
```
python3 web_scraper.py client [HOSTNAME] [-PORT] -p [Webpage URL]
```
You can provide [Webpage URL] both with 'http(s)://' and without it.