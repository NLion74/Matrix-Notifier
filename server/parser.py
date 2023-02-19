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


def headerparse(headers):
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
                return "wrong_markdown"
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


def queryparse(queries):
    # Defaults
    message = "webhook triggered"
    title = ""
    channels = []
    auth_pass = ""
    markdown = "false"
    parsed_tags = []

    for query, query_content in queries.items():
        if query == "X-Message" or query.lower() == "message" or query.lower() == "ms":
            message = query_content
        if query == "X-Title" or query.lower() == "title" or query.lower() == "t":
            title = query_content
        elif query == "X-Channel" or query.lower() == "channel" or query.lower() == "c":
            if "," in query_content:
                temp_channels = query_content.rsplit(",")
                for channel in temp_channels:
                    channels.append(channel)
            else:
                channels.append(query_content)
        elif query == "X-Authorization" or query.lower() == "authorization" or query.lower() == "auth":
            auth_pass = query_content
        elif query == "X-Markdown" or query.lower() == "markdown" or query.lower() == "m":
            if str(query_content).lower() == "true" or str(query_content).lower() == "false":
                markdown = str(query_content).lower()
            else:
                return "wrong_markdown", "wrong_markdown"
        elif query == "X-Tags" or query.lower() == "tags" or query.lower() == "tag" or query.lower() == "ta":
            tags = query_content.rsplit(",")
            parsed_tags = []
            for tag in tags:
                tag = str(tag).lower()
                tag = remove_spaces(tag)
                parsed_tags.append(tag)

    parameter = ParaMeter(title=title, channels=channels,
                          auth_pass=auth_pass, markdown=markdown,
                          tags=parsed_tags)

    return parameter, message


def webhookmessageparse(parameter, content):
    msg = Message(title=parameter.title, content=content,
                  channels=parameter.channels, markdown=parameter.markdown,
                  tags=parameter.tags)
    return msg
