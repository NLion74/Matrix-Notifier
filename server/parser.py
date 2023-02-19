from dataclasses import dataclass
import logging

logger = logging.getLogger()


@dataclass
class ParaMeter:
    channels: list
    title: str
    auth_pass: str
    tags: list
    markdown: str


@dataclass
class Message:
    channels: list
    title: str
    content: str
    tags: list
    markdown: str


def remove_spaces(tag):
    if str(tag).startswith(" "):
        tag = tag[1::]
        tag = remove_spaces(tag)
    return tag


def parameterparse(headers):
    # Defaults
    title = ""
    channels = []
    auth_pass = ""
    markdown = "false"
    parsed_tags = []

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
        elif header == "X-Markdown" or header.lower() == "markdown" or header.lower() == "m":
            if str(header_content).lower() == "true" or str(header_content).lower() == "false":
                markdown = str(header_content).lower()
            else:
                return False
        elif header == "X-Tags" or header.lower() == "tags" or header.lower() == "tag" or header.lower() == "ta":
            tags = header_content.rsplit(",")
            parsed_tags = []
            for tag in tags:
                tag = str(tag).lower()
                tag = remove_spaces(tag)
                parsed_tags.append(tag)


    parameter = ParaMeter(title=title, channels=channels,
                          auth_pass=auth_pass, markdown=markdown,
                          tags=parsed_tags)

    return parameter


def messageparse(parameter, body):
    content = ""
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
                  channels=parameter.channels, markdown=parameter.markdown,
                  tags=parameter.tags)
    return msg
