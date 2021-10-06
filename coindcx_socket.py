# Python3
# import socketio
# import socket # for socket 
# import sys
import socketio

socketEndpoint = 'wss://stream.coindcx.com'
sio = socketio.Client()
# sio=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sio.connect(socketEndpoint, transports = 'websocket')
sio.emit('join', { 'channelName': 'coindcx','channel': "B-XRP_ETH", "event": "depth-update"})

# # Listen update on channelName
# @sio.on('channelName')
# def on_message(response):
#     print(response.data)

# # leave a channel
# sio.emit('leave', { 'channelName' : channelName })

@sio.on('depth-update')
def on_message(response):
    print(response.data.a) # asks
    print(response.data.b) # bids