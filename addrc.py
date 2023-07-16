import asyncio
import datetime
import json
import time
import websockets
from typing import Union
from tools import log, get_ws_name, get_tail, msg_handle
from config import self_id, ws_addrs

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

    @property
    def uri(self) -> str:
        return self.uris[0]

    @property
    async def start_connect(self):
        await self.set_self_id()
        self.connection = await websockets.connect(
            self.uri,
            extra_headers=self.extra_headers,
        )

    async def set_self_id(self):
        while self.self_id == "":
            self.self_id = await self.get_self_id()
        self.extra_headers["X-Self-Id"] = self.self_id
        print(f"0：{self.name} self_id is {self.self_id}")

    async def send(self, message):
        await self.connection.send(message)

    # @property
    async def recv_to_forward(self):
        while True:
            # usually only one ws
            log(f"0:Waiting for response from {self.name}...")
            response = await self.connection.recv()
            log(
                f"1：Response from {self.name} forwarded to client: {response}",
            )
            response = msg_handle(self.name, response)
            log(f"2：Response from {self.name} forwarded to client: {response} ")
            self.send_to_client(response)
            # for websocket in self.connected:
            #     await websocket.send(response)

    # async def connect_old(self):
    #     global ws_connections

    #     ws_connections[f"{self.uri}_{self.self_id}"] = await websockets.connect(
    #         self.uri,
    #         xtra_headers=self.extra_headers,
    #     )
