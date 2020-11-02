# Client-Server based TCP text service console application

## Scenario
You as a software developer must create the client-server-based console app “text_service”.
With the next abilities:
* Change text: The sender sends the text file to the server and the json file, in respond the server
must read the json file and swap the words from the text according the json file.
* Encode/Decode text: The sender sends the text file and the key (another text) on the respond
the server must XOR the text message with the key (One Time Pad cipher) and return it to the
client. The decoding process happens in the same way where instead of the text message the
client send
## Installation
```
git clone https://github.com/familbabayev/Network_Programming/tree/master/Lab2(TCP_Textservice)
```
Application uses built-in python 3.7.4 packages. No additional requirements.

## Usage
For server:
```
python3 TCP_Textservice.py server "" [-p]
```
For client:

```
python3 UDP_Backoff_OOP.py client [hostname] [-p] --mode change_text source_file.txt json_file.json
```
```
python3 UDP_Backoff_OOP.py client [hostname] [-p] --mode encode_decode source_file.txt otp_key.txt
```
The default value(1060) for port number is assigned by the program, so you can omit it.  