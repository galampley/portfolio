// Function to send a message to the server and get the response
function sendMessage(message) {

    $('#loading-spinner').show();

    $.ajax({
        url: '/chat',  // URL of your Flask route
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'message': message }),
        success: function(response) {
            console.log(response);
            $('#loading-spinner').hide();

            // Append the response to your chat window
            $('#chat-window').append(`<div class="bot-message">${response}</div>`);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

// Event handler for sending a message
$('#send-button').click(function() {
    var userMessage = $('#message-input').val();
    $('#chat-window').append(`<div class="user-message">${userMessage}</div>`); // Show user message in chat window
    sendMessage(userMessage);
    $('#message-input').val(''); // Clear the input field
});

$(document).ready(function() {
    $('#chatbot-container').addClass('collapsed'); // Start with the chat window collapsed

    // Toggle the chat window and icon visibility
    $('#chatbot-icon').click(function() {
        $('#chatbot-container').toggleClass('collapsed expanded');
        $('#chatbot-icon').css('opacity', '1'); // Ensure the icon is visible when the chat window is collapsed
    });

    $('#chat-window').append(`<div class="bot-message">Hello there, I'm Greyson's Portfolio Wiz. Ask some questions about his experience, skills, or blog.</div>`);
});
