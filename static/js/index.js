$(document).ready(function(){
    let hasher_uri = $('#hasher').attr('action');
    let host = $(location).attr('host');
    let protocol =  $(location).attr('protocol') + '//';

    $('#generate').on('click', function(e){
        e.preventDefault();
       
        $('#hasher #key').val( gen_key(32));
    });


    $('#hasher').on('submit', function(e){
        e.preventDefault();

        let url = protocol + host + hasher_uri;
        let form_data = $('#hasher');


        let data = {
            hasher: $('input[name=hasher_mode]:checked', '#hasher').val(),
            key: form_data.find('#key').val(),
            key_type: $('input[name=key_type]:checked', '#hasher').val(),
            message: form_data.find('#message').val(),
            message_type: $('input[name=msg_type]:checked', '#hasher').val(),
        };

        let request = $.ajax({
            method: 'POST',
            url: url,
            data: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json"
            },
        });
        request.done(function(response){
            $('#result').removeClass('alert alert-success');
            $('#result').addClass('alert alert-danger');
            if (response.error) {
                let result = Object.values(response.error).join('<br/>');
                $('#result').html('<b>Some errors happen:</b><br>' + result);
            }
            else{
                $('#result').removeClass('alert alert-danger');
                $('#result').addClass('alert alert-success');
                $('#result').html('<b>Your hash:</b><br>' + response.hash);
            }
        });
    });

    $('#verif_btn').on('click', function(e){
        e.preventDefault();
        e.preventDefault();
        let url = protocol + host + hasher_uri;
        let form_data = $('#hasher');

        let data = {
            hasher: $('input[name=hasher_mode]:checked', '#hasher').val(),
            key: form_data.find('#key').val(),
            key_type: $('input[name=key_type]:checked', '#hasher').val(),
            message: form_data.find('#message').val(),
            message_type: $('input[name=msg_type]:checked', '#hasher').val(),
        };

        let request = $.ajax({
            method: 'POST',
            url: url,
            data: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json"
            },
        });
        request.done(function(response){
            $('#result').removeClass('alert alert-success');
            $('#result').addClass('alert alert-danger');
            if (response.error) {
                let result = Object.values(response.error).join('<br/>');
                $('#result').html('<b>Some errors happen:</b><br>' + result);
            }
            else{
                let answer = "<b>INVALID</b>"
                if (response.hash == $('#verification').val()){
                    answer = "<b>VALID</b>"
                    $('#result').removeClass('alert alert-danger');
                    $('#result').addClass('alert alert-success');
                }
                $('#result').html('<b>Your hash is:</b><br>' + answer);
            }
        });
        
    });

    function gen_key(length){

        let result = new Array(length)
        let idx = 0;
        const alphanum = '0123456789abcdefghijklmnopqrstuvwxyz';
        for (let i = 0; i < length; i++) {
            idx = Math.floor(Math.random() * (35 - 0 + 1) );
            result[i] = alphanum[idx];
        }
        return result.join('');
    }
        
});

