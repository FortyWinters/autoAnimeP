$(function() {
    $('button.start-button').on('click', function() {
        console.log('start')
        this.disabled = true;
        this.style.backgroundColor = "#d6d6d6";

        var interval = 2

        fetch("/setting/start_main_task?interval=" + interval, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            console.log(data)
            this.disabled = false;
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });

    });

    $('button.stop-button').on('click', function() {
        console.log('stop')

    });

    $('button.modify-button').on('click', function() {
        console.log('modify')

    });
})