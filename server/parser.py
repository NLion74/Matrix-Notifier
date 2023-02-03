from dataclasses import dataclass


@dataclass
class HttpRequest:
    method: str
    uri: str
    version: str
    headers: list
    body: str


@dataclass
class ParaMeter:
    channel: []
    title: str


@dataclass
class Message:
    channel: []
    title: str
    content: str


def httparse(r):
    r = str(r)
    r = r[2::]
    r = r[:-1]
    r = str(r).rsplit("\\r\\n\\r\\n")
    request_data = r[0]
    body = r[1]
    r = request_data.split("\\r\\n", 1)
    status_line = r[0]
    s = status_line.rsplit(" ")
    method = s[0]
    uri = s[1]
    version = s[2]

    headers_raw = r[1]
    h = headers_raw.rsplit("\\r\\n")
    headers = []
    for header in h:
        headers.append(header)

    rq = HttpRequest(method=method, uri=uri, version=version, headers=headers, body=body)

    return rq


def headerparse(rq):
    # Defaults
    title = ""
    channel = []

    for header in rq.headers:
        header = str(header)
        try:
            h = header.rsplit(": ", 1)
            parameter = h[0]
            option = h[1]
        except IndexError:
            try:
                h = header.rsplit(":", 1)
                parameter = h[0]
                option = h[1]
            except IndexError:
                print("Invalid header")

        if parameter == "X-Title" or parameter.lower() == "title" or parameter.lower() == "t":
            title = option
        elif parameter == "X-Channel" or parameter.lower() == "channel" or parameter.lower() == "c":
            channel.append(option)

    parameter = ParaMeter(title=title, channel=channel)

    return parameter


def messageparse(rq, parameter):
    msg = Message(title=parameter.title, content=rq.body, channel=parameter.channel)
    return msg
