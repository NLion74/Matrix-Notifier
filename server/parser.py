from dataclasses import dataclass
import logging

logger = logging.getLogger()


@dataclass
class HttpRequest:
    method: str
    uri: str
    version: str
    headers: list
    body: str


@dataclass
class ParaMeter:
    channels: list
    title: str
    auth_pass: str


@dataclass
class Message:
    channels: list
    title: str
    content: str


def headerparse(headers):
    # Defaults
    title = ""
    channels = []
    auth_pass = ""

    for header, header_content in headers.items():
        if header == "X-Title" or header.lower() == "title" or header.lower() == "t":
            title = header_content
        elif header == "X-Channel" or header.lower() == "channel" or header.lower() == "c":
            if "," in header_content:
                temp_channels = header_content.rsplit(",")
                for channel in temp_channels:
                    channels.append(channel)
            else:
                channels.append(header_content)
        elif header == "X-Authorization" or header.lower() == "authorization" or header.lower() == "auth":
            auth_pass = header_content

    parameter = ParaMeter(title=title, channels=channels, auth_pass=auth_pass)

    return parameter


def messageparse(parameter, body):
    try:
        content = body.decode("utf-8")
    except UnicodeError:
        logger.error("Client doesn't seem to be using valid utf-8")
        try:
            content = body.decode("cp932")
        except UnicodeError:
            try:
                content = body.decode("ascii")
            except UnicodeError:
                try:
                    content = body.decode("ISO-8859-1")
                except UnicodeError:
                    logger.error("Couldn't decode request data")

    msg = Message(title=parameter.title, content=content,
                  channels=parameter.channels)
    return msg
