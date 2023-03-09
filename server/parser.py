from dataclasses import dataclass
import logging
import json

logger = logging.getLogger(__name__)


@dataclass
class ParaMeter:
    channels: list
    title: str
    auth_pass: str
    tags: list
    markdown: str
    limit: int


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
    limit = 100

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
                          tags=parsed_tags, limit=limit)

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
    limit = 100

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
        elif query == "X-Limit" or query.lower() == "limit" or query.lower() == "l":
            limit = query_content

    parameter = ParaMeter(title=title, channels=channels,
                          auth_pass=auth_pass, markdown=markdown,
                          tags=parsed_tags, limit=limit)

    return parameter, message


def webhookmessageparse(parameter, content):
    msg = Message(title=parameter.title, content=content,
                  channels=parameter.channels, markdown=parameter.markdown,
                  tags=parameter.tags)
    return msg

def jsonparse(body):
    # Defaults
    message = ""
    title = ""
    channels = []
    auth_pass = ""
    markdown = "false"
    parsed_tags = []
    limit = 100

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

    try:
        json_body = json.loads(content)
    except json.JSONDecodeError:
        return "JSONDecodeError", "JSONDecodeError"

    for key, value in json_body.items():
        if key == "X-Message" or key.lower() == "message" or key.lower() == "ms":
            message = value
        if key == "X-Title" or key.lower() == "title" or key.lower() == "t":
            title = value
        elif key == "X-Channel" or key.lower() == "channel" or key.lower() == "c":
            channels.append(value)
        elif key == "X-Authorization" or key.lower() == "authorization" or key.lower() == "auth":
            auth_pass = value
        elif key == "X-Markdown" or key.lower() == "markdown" or key.lower() == "m":
            if str(value).lower() == "true" or str(value).lower() == "false":
                markdown = str(value).lower()
            else:
                return "wrong_markdown", "wrong_markdown"
        elif key == "X-Tags" or key.lower() == "tags" or key.lower() == "tag" or key.lower() == "ta":
            tags = value.rsplit(",")
            parsed_tags = []
            for tag in tags:
                tag = str(tag).lower()
                tag = remove_spaces(tag)
                parsed_tags.append(tag)

    if message == "":
        return "message required", "message required"

    parameter = ParaMeter(title=title, channels=channels,
                          auth_pass=auth_pass, markdown=markdown,
                          tags=parsed_tags, limit=limit)

    return parameter, message
