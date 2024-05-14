function deleteMessage(messageId) {
  /* This function extracts and sends the message ID to the /delete route
    It sends a post request to the /delete route
    The messageID key has the id of the message to be deleted
    After that, it reloads the window
    */
  fetch("/delete", {
    method: "POST",
    body: JSON.stringify({ messageId: parseInt(messageId) }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
