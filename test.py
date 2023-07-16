# Unicode 转义序列到 UTF-8 的转换
def unicode_escape_to_utf8(s):
    return bytes(s, "utf-8").decode("unicode_escape")


# UTF-8 到 Unicode 转义序列的转换
def utf8_to_unicode_escape(s):
    return s.encode("unicode_escape").decode("utf-8")


# 测试上述函数
s = r"\u4f60\u597d"  # 使用原始字符串
print(type(s))
b = unicode_escape_to_utf8(s)
print(b)
b += "你好"
s2 = utf8_to_unicode_escape(b)
print(s2)

print(unicode_escape_to_utf8(s2))
a = {"a": 1, "b": 2}
a.update({"c": 3})
a.update({"a": 4})
print(a)

h = {
    "meta_event_type": "lifecycle",
    "post_type": "meta_event",
    "self_id": 2470666214,
    "sub_type": "connect",
    "time": 1689412627,
}

null = None
a = {
    "post_type": "message",
    "message_type": "group",
    "time": 1689430807,
    "self_id": 2470666214,
    "sub_type": "normal",
    "message": [{"type": "text", "data": {"text": "螺旋太简单了"}}],
    "raw_message": "螺旋太简单了",
    "user_id": 1067117520,
    "message_id": 398241490,
    "anonymous": null,
    "font": 0,
    "group_id": 929275476,
    "message_seq": 631742,
    "sender": {
        "age": 0,
        "area": "",
        "card": "",
        "level": "",
        "nickname": "鱼日匀",
        "role": "member",
        "sex": "unknown",
        "title": "",
        "user_id": 1067117520,
    },
}

s = {
    "post_type": "message",
    "message_type": "group",
    "time": 1689431079,
    "self_id": 2470666214,
    "sub_type": "normal",
    "message_seq": 953824,
    "sender": {
        "age": 0,
        "area": "",
        "card": "Sam酱鸭",
        "level": "",
        "nickname": "Sam酱",
        "role": "owner",
        "sex": "unknown",
        "title": "可爱又帅气的",
        "user_id": 1102566608,
    },
    "user_id": 1102566608,
    "message_id": 1097363884,
    "group_id": 790121399,
    "message": "帮助",
    "raw_message": "帮助",
    "anonymous": null,
    "font": 0,
}

s2 = {
    "post_type": "message",
    "message_type": "group",
    "time": 1689431176,
    "self_id": 2470666214,
    "sub_type": "normal",
    "message": "帮助[CQ:image,file=b169a9026e88f5a870d6676a6be6a298.image,subType=1,url=https://gchat.qpic.cn/gchatpic_new/1102566608/790121399-2474049848-B169A9026E88F5A870D6676A6BE6A298/0?term=255\u0026amp;is_origin=1]",
    "message_seq": 953832,
    "raw_message": "帮助[CQ:image,file=b169a9026e88f5a870d6676a6be6a298.image,subType=1,url=https://gchat.qpic.cn/gchatpic_new/1102566608/790121399-2474049848-B169A9026E88F5A870D6676A6BE6A298/0?term=255\u0026amp;is_origin=1]",
    "user_id": 1102566608,
    "anonymous": null,
    "font": 0,
    "group_id": 790121399,
    "sender": {
        "age": 0,
        "area": "",
        "card": "Sam酱鸭",
        "level": "",
        "nickname": "Sam酱",
        "role": "owner",
        "sex": "unknown",
        "title": "可爱又帅气的",
        "user_id": 1102566608,
    },
    "message_id": -1324292648,
}


sr = {
    "action": ".handle_quick_operation_async",
    "params": {
        "self_id": 2470666214,
        "context": {
            "post_type": "message",
            "message_type": "group",
            "time": 1689431401,
            "self_id": 2470666214,
            "sub_type": "normal",
            "user_id": 1102566608,
            "anonymous": null,
            "font": 0,
            "group_id": 600181960,
            "message_seq": 6863,
            "message_id": -1617168257,
        },
        "operation": {
            "reply": "\u53c8\u4e0d\u7533\u8bf7\ufeff\u51fa\u5200\u53c8\u4e0d\u8bf4\u6253\u54ea\ufeff\u4e2a\u738b\uff0c\ufeff\u62a5\u5565\u5b50\u5200\u554a (\u256f\u2035\u25a1\u2032)\u256f\ufe35\u253b\u2501\u253b",
            "at_sender": False,
        },
    },
    "echo": {"seq": 41},
}


ar = {
    "action": "send_msg",
    "params": {
        "user_id": 1102566608,
        "group_id": 600181960,
        "message_type": "group",
        "message": [
            {"type": "at", "data": {"qq": "1102566608"}},
            {"type": "text", "data": {"text": " "}},
            {
                "type": "text",
                "data": {
                    "text": '\u7fa4\u5185\u8fd8\u672a\u5f00\u542f\u6deb\u8db4\u6e38\u620f, \u8bf7\u7ba1\u7406\u5458\u6216\u7fa4\u4e3b\u53d1\u9001"\u5f00\u542f\u6deb\u8db4", "\u7981\u6b62\u6deb\u8db4"\u4ee5\u5f00\u542f/\u5173\u95ed\u8be5\u529f\u80fd'
                },
            },
        ],
    },
    "echo": "3180",
}
