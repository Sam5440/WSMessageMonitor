
import asyncio
import datetime
import json
import time
import websockets
from typing import Union
from tools import log, get_ws_name, get_tail, msg_handle
from config import ws_addrs,debug
from addrc import WebSocketClient, YunzaiWs


# Start:连接gocq的ws server 
connected,self_id = set(),""
async def server(websocket):
    # Register.
    global self_id
    connected.add(websocket)
    try:
        headers = dict(websocket.request_headers)
        self_id = headers["x-self-id"]
        log(f"H：Headers from client: {headers} ")
        async for message in websocket:
            if "1102566608" not in message and debug:
                continue
            log(f"0：Received message from client:{type(message)}-{message}")
            await send_to_other_ws(message)
    finally:
        log("4：Connection closed")
        connected.remove(websocket)
# End:连接gocq的ws server 


async def send_to_other_ws(message):
    #消息转发到需要连接的ws后端
    if ws_connections:
        push_ws = []
        for ws_name, ws in ws_connections.items():
            try:
                await ws.send(message)
                push_ws.append(ws_name)
            except Exception as e:
                log(f"Send msg to{ws_name} is missing: {e}")
        log(f"1：Message forwarded to {push_ws}")

def send_to_client(message):
    # 消息转发到gocq端
    if connected:
        for ws in connected:
            asyncio.create_task(ws.send(message))
async def get_self_id():
    # 从连接的gocq的哪里获得self_id
    while self_id  in ["","0","114514"] or self_id is None:
        await asyncio.sleep(1)
    return self_id
ws_connect_tasks , recv_tasks ,ws_connections= [],[],{}
for ws_name, ws_addr in ws_addrs.items():
    # 创建后端ws连接与消息接收coroutine
    if ws_name not in ["yunzai"]:
        ws_connections[ws_name]  = WebSocketClient(ws_name, ws_addr,send_to_client=send_to_client,get_self_id=get_self_id)
    else:
        ws_connections[ws_name]  = YunzaiWs(ws_name, ws_addr,send_to_client=send_to_client)
    ws_connect_tasks.append(ws_connections[ws_name].start_connect)
    recv_tasks.append(ws_connections[ws_name].recv_to_forward())
    # log(f"0：{ws_name} Connected to {ws_addr} successfully!")
start_server = websockets.serve(server, "localhost", 40018,max_size=10**10)
asyncio.get_event_loop().run_until_complete(asyncio.gather(start_server))    
asyncio.get_event_loop().run_until_complete(asyncio.gather(*ws_connect_tasks))
asyncio.get_event_loop().run_until_complete(asyncio.gather(*recv_tasks))
asyncio.get_event_loop().run_forever()
