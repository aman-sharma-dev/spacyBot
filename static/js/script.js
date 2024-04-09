document.addEventListener('DOMContentLoaded', function () {
    var messageArea = document.getElementById('messageArea');
    var textInput = document.getElementById('text');
    var messageFormeight = document.getElementById('messageFormeight');
    var messageSentSound = new Audio('/static/audio/happy-pop-2-185287.mp3');
    var botReplySound = new Audio('/static/audio/multi-pop-6-188170.mp3');

    messageArea.addEventListener('submit', function (event) {
        var date = new Date();
        var hour = date.getHours();
        var minute = date.getMinutes();
        var str_time = hour + ":" + minute;

        var rawText = textInput.value;

        var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + rawText + '<span class="msg_time_send">' + str_time + '</span></div><div class="img_cont_msg"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M399 384.2C376.9 345.8 335.4 320 288 320H224c-47.4 0-88.9 25.8-111 64.2c35.2 39.2 86.2 63.8 143 63.8s107.8-24.7 143-63.8zM0 256a256 256 0 1 1 512 0A256 256 0 1 1 0 256zm256 16a72 72 0 1 0 0-144 72 72 0 1 0 0 144z"/></svg></div></div>';

        textInput.value = '';
        messageFormeight.insertAdjacentHTML('beforeend', userHtml);
        messageSentSound.play();

        // Show loading animation
        showLoadingAnimation();

        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                // Hide loading animation once response is received
                hideLoadingAnimation();

                if (xhr.status == 200) {
                    var data = xhr.responseText;
                    var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="./static/images/chatbot.jpg" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' + data + '<span class="msg_time">' + str_time + '</span></div></div>';

                    messageFormeight.insertAdjacentHTML('beforeend', botHtml);
                    playBotReplySound(); 
                } else if (xhr.status == 429) {
                    console.error('Error 429: Too Many Requests');
                    // Display loading animation again or show an error message indicating too many requests
                } else {
                    console.error('Error:', xhr.statusText);
                }
            }
        };

        xhr.open('POST', '/get', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        var postData = 'msg=' + encodeURIComponent(rawText);
        xhr.send(postData);

        event.preventDefault();
    });

    textInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            messageArea.dispatchEvent(new Event('submit'));
        }
    });

    function playBotReplySound() {
        botReplySound.play();
    }

    function showLoadingAnimation() {
        var loadingDiv = document.createElement('div');
        loadingDiv.id = 'loading';
        loadingDiv.className = 'loading';
        loadingDiv.innerHTML = '<div id="loading" class="loading-container"><div class="snippet" data-title="dot-typing"><div class="stage"><div class="dot-typing"></div></div></div></div>';
        messageFormeight.appendChild(loadingDiv);
    }

    function hideLoadingAnimation() {
        var loadingDiv = document.getElementById('loading');
        if (loadingDiv) {
            loadingDiv.parentNode.removeChild(loadingDiv);
        }
    }
});
