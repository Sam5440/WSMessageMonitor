import datetime, json
from config import msg_tail, ws_addrs


def log(msg):
    # 保存到文件 daily.log
    with open("daily.log", "a",encoding="utf-8") as f:
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now_time}]{msg}\n")
    if len(msg) < 1_000:
        print(msg)


def get_ws_name(ws_addr):
    return [k for k, v in ws_addrs.items() if v == ws_addr][0]


def get_tail(ws_name):
    return msg_tail + f"\n From [{ws_name}]"


def msg_handle(ws_name, response):
    return response
    try:
        response = json.loads(response)
        if response["params"].get("message_type"):
            log(f'debug {response["params"]["message"]}')
            response["params"]["message"].append(
                {"type": "text", "data": {"text": get_tail(ws_name)}}
            )
        if response["params"].get("operation"):
            response["params"]["operation"]["reply"] += get_tail(ws_name)
    except KeyError:
        log("3：Key Error of Response")
    except Exception as e:
        log(e)
    return json.dumps(response)
