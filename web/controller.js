document.getElementById('run').addEventListener('click', function(event) {
    let x = document.getElementById('X_coordinate').value;
    let y = document.getElementById('Y_coordinate').value;
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            console.log('done');
        }
    }
    xhttp.open('POST', '', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(JSON.stringify({x: x, y: y}));
});