async function make_request(message, title, tags, token, channel, markdown) {
    if (title !== "" || tags !== "") {
        console.log("t")
        const res = await fetch('/', {
            method: 'POST',
            headers: {
                'Authorization': token,
                'Channel': channel,
                'Title': title,
                'Tags': tags,
                'Markdown': markdown
            },
            body: (message)
        })
        return res;
    }
    else {
        const res = await fetch('/', {
            method: 'POST',
            headers: {
                'Authorization': token,
                'Channel': channel,
                'Markdown': markdown
            },
            body: (message)
        })
        return res;
    }
}

function check_checkbox(checkbox)  {
    if (checkbox.checked) {
        return "true";
    }
    else {
        return "false";
    }
}

const onSubmit = async (e) => {
    e.preventDefault();

    msgSuccessDiv.innerText = "";
    msgErrorDiv.innerText = "";

    sendButton.disabled = true;

    const message = messageInput.value;
    const title = titleInput.value;
    const tags = tagsInput.value;
    const token = window.tokenInput?.value;
    const channel = channelInput.value;
    const markdown = check_checkbox(markdownCheckbox);

    const res = await make_request(message, title, tags, token, channel, markdown)

    if (res.status !== 200) {
        const text = await res.text();
        msgErrorDiv.innerText = text || res.statusText;
    }
    else {
        msgSuccessDiv.innerText = "Message send";
        messageInput.value = "";
        titleInput.value = "";
        tagsInput.value = "";
    }

    sendButton.disabled = false;
}

form.onsubmit = onSubmit;
