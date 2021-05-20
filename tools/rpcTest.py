import pyjsonrpc

link = raw_input('Please enter the RPC IP address: ') or 'http://localhost:8080'
token = raw_input('Please enter your RPC token: ') or 'test'
data = raw_input("Please enter some data you'd like to get back: ") or 'Pink fluffy unicorns'
client = pyjsonrpc.HttpClient(url = link)

print
print client.ping(token, data)