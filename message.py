import json

class Message:

    def __init__(self, id, send_ts, ip_address, user_name, type, content):
        self.id = id
        self.send_ts = send_ts
        self.ip_address = ip_address
        self.user_name = user_name
        self.type =type
        self.content = content

    def to_json(self):
        json_dict = {}
        for attr in self.__dict__:
            json_dict[attr] = getattr(self, attr)
        return json.dumps(json_dict)

if __name__ == "__main__":
    msg = Message(1, 'datetime', 'iphere', 'bobdylan', 'text', "Here is my text/blob")
    x = msg.to_json()
    pass