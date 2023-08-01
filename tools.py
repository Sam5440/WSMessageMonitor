import datetime, json
from config import msg_tail, ws_addrs
log_level = 1
time_start = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def log(msg,level=3,log_file_name=None):
    # 保存到文件 daily.log
    file_name = time_start if log_file_name is None else f"{log_file_name}_{time_start}"
    if len(msg) < 1_000 and level <= log_level:
        with open(f"log/{file_name}.log", "a",encoding="utf-8") as f:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now_time}]{msg}\n")
            print(f"[{now_time}]{msg}")


def get_ws_name(ws_addr):
    return [k for k, v in ws_addrs.items() if v == ws_addr][0]


def get_tail(ws_name):
    return msg_tail + f"\n From [{ws_name}]"


def msg_handle(ws_name, response):
    # return response
    try:
        response = json.loads(response)
        if response.get("params"):
            if response["params"].get("message"): #if response["params"].get("message_type"):
                log(f'debug {response["params"]["message"]}',3)
                response["params"]["message"].append(
                    {"type": "text", "data": {"text": get_tail(ws_name)}}
                )
            if response["params"].get("operation"):
                response["params"]["operation"]["reply"] += get_tail(ws_name)
    except KeyError:
        log("3：Key Error of Response",1)
    except Exception as e:
        log(e,1)
    return json.dumps(response)
