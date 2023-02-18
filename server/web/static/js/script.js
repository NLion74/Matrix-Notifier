function check_checkbox(checkbox)  {
    console.log(checkbox)
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
    const token = window.tokenInput?.value;
    const channel = channelInput.value;
    const markdown = check_checkbox(markdownCheckbox);

    console.log(markdown);

    const res = await fetch('/', {
        method: 'POST',
        headers: {
            Authorization: token,
            Channel: channel,
            Title: title,
            Markdown: markdown
        },
        body: (message)
    })

    if (res.status !== 200) {
        const text = await res.text();
        msgErrorDiv.innerText = text || res.statusText;
    }
    else {
        msgSuccessDiv.innerText = "Message send";
        messageInput.value = "";
        titleInput.value = "";
    }

    sendButton.disabled = false;
}

form.onsubmit = onSubmit;
