import datetime, json
from config import msg_tail, ws_addrs
log_level = 1
time_start = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def log(msg,level=3,log_file_name=None):
    # 保存到文件 daily.log
    
    msg = str(msg)
    
    file_name = time_start if log_file_name is None else f"{log_file_name}_{time_start}"
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if len(msg) < 1_000 and level <= log_level:
        print(f"[{now_time}]{msg}")
    with open(f"F:/log/{file_name}.log", "a",encoding="utf-8") as f:
        f.write(f"[{now_time}]{msg}\n")

def get_ws_name(ws_addr):
    return [k for k, v in ws_addrs.items() if v == ws_addr][0]


def get_tail(ws_name):
    return msg_tail + f"\n From [{ws_name}]"


def msg_handle(ws_name, response):
    # return response
    log(response)
    try:
        response = json.loads(response)
        if response.get("params"):
            if response["params"].get("message"): #if response["params"].get("message_type"):
                log(f'debug {response["params"]["message"]}',3)
                if isinstance(response["params"]["message"],str):
                    response["params"]["message"] += get_tail(ws_name)
                else:
                    response["params"]["message"].append(
                        {"type": "text", "data": {"text": get_tail(ws_name)}}
                    )
            if response["params"].get("operation"):
                response["params"]["operation"]["reply"] += get_tail(ws_name)
    except KeyError:
        log("3：Key Error of Response",1)
    except Exception as e:
        log(str(e)+str(response),1,log_file_name="e")
        raise "a"
    return json.dumps(response)
