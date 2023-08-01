import asyncio
import datetime
import json
import time
import websockets
from typing import Union
from tools import log, get_ws_name, get_tail, msg_handle
from config import  ws_addrs

# from main import connected


class WebSocketClient:
    def __init__(
        self,
        name: str,
        uris: Union[list, str],
        self_id: str = None,
        extra_headers: dict = {},
        # func
        send_to_client: callable = None,
        get_self_id: callable = None,
    ):
        self.get_self_id = get_self_id
        self.send_to_client = send_to_client
        self.name = name
        self.uris = uris if isinstance(uris, list) else [uris]
        self.extra_headers = extra_headers if extra_headers else {"X-Self-Id": self_id}
        self.self_id = self.extra_headers["X-Self-Id"]
        default_headers = {
            "X-Client-Role": "Universal",
            "user-agent": "CQHttp/4.15.0",
        }
        self.extra_headers.update(default_headers)
        self.msg_cache = []
        self.connection = None
        self.coro_lock = False
        
        
    @property
    def uri(self) -> str:
        #随机获得一个uri来做负载均衡
        return self.uris[0]

    @property
    async def start_connect(self):
        if not self.coro_lock:
            self.coro_lock = True
            try:
                # 连接，启动！
                await self.set_self_id()
                log(f"addrL43：{self.name} Connecting to {self.uri} {self.extra_headers}...",3)
                self.connection = await websockets.connect(
                    self.uri,
                    extra_headers=self.extra_headers,
                    max_size=10**10
                )
                # await asyncio.sleep(3)
                log(f"addrL56：{self.name} Connected to {self.uri} successfully!", 3)
                # break  # Add this line
            except (websockets.exceptions.ConnectionClosed, OSError):
                log(f"addrL59：Failed to connect to {self.uri}. Retrying in 5 seconds...", 3)
                await asyncio.sleep(3)  # Add this line
            except Exception as e:
                log(f"addrL62：Failed to connect to {self.uri}. Retrying in 5 seconds...", 3)
                log(e,1)
            finally:
                self.coro_lock = False
                
                # await asyncio.sleep(3)  # Add this line
                
    # async def start_connect(self):
    #     # 连接，启动！
    #     await self.set_self_id()
    #     log(f"addrL43：{self.name} Connecting to {self.uri} {self.extra_headers}...",3)
    #     self.connection = await websockets.connect(
    #         self.uri,
    #         extra_headers=self.extra_headers,
    #         max_size=10**10
    #     )

    async def set_self_id(self):
        # 从gocq的header头获得self_id
        if self.self_id == "" or self.self_id is None:
            self.self_id = await self.get_self_id()
        # self.self_id = "2470666214"
        # self.self_id = await self.get_self_id()
        log(f"addrL54：{self.name} self_id is {self.self_id}",3)
        self.extra_headers["X-Self-Id"] = self.self_id
        log(f"addrL79：{self.name} self_id is {self.self_id}",1)

    async def send(self, message):
        # 向ws推送消息
        self.msg_cache.append(message)
        # log(f"msg_cache:{self.msg_cache}")
        if self.connection:
            for msg in self.msg_cache:
                await self.connection.send(msg)
                await asyncio.sleep(0.001)
            self.msg_cache = []
        await asyncio.sleep(0.001)
        
            

    # @property
    async def recv_to_forward(self):
        # 接收消息并且转发到gocq
        while True:
            # usually only one ws
            log(f"0:Waiting for response from {self.name}...",3)
            try:
                response = await self.connection.recv()
            except Exception as e:
                # log(f"recv failed [{self.name}]",1)
                await asyncio.sleep(0.001)
                continue
            log(self.name,3)
            log(
                f"1：Response from {self.name} forwarded to client: {response}",2
            )
            response = msg_handle(self.name, response)
            log(f"2：Response from {self.name} forwarded to client: {response} ",3)
            self.send_to_client(response)

    # async def connect_old(self):
    #     global ws_connections

    #     ws_connections[f"{self.uri}_{self.self_id}"] = await websockets.connect(
    #         self.uri,
    #         xtra_headers=self.extra_headers,
    #     )
class YunzaiWs(WebSocketClient):
    # yunzai 不能带self_id
    async def set_self_id(self):
        # await asyncio.sleep(0.1)
        self.self_id = None
        # self.self_id = await self.get_self_id()
        log(f"addrL54：{self.name} self_id is {self.self_id}",3)
        self.extra_headers["X-Self-Id"] = self.self_id
        print(f"0：{self.name} self_id is {self.self_id}")