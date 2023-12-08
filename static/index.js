console.log('Hello from static/index.js');


function niceButtonFunction() {
    console.log("Nice button clicked!");
    fetch('/api/example_endpoint', {
        method: 'GET',
    }).then(response => response.json().then(data => {

        console.log(data);

        // get message p element
        const messageElement = document.getElementById('message');
        // update message
        messageElement.innerText = data.message;

        // get count p element
        const countElement = document.getElementById('count');
        // update count
        countElement.innerText = data.count;
    }))
}
