$(document).ready(function(){
    let host = $(location).attr('protocol') + '//' + $(location).attr('host');
    let uri = '';
    let action = '';
    let url = '';
    let mode = 'Empty'

    let keys = {};
    let params = {};
    let signature = {};

    let keys_ready = false;

    const RSA_btn = $('#rsa');
    const DSA_btn = $('#dsa');
    const RSA_CHECK_btn = $('#verify-rsa')
    const DSA_CHECK_btn = $('#verify-dsa')
    const WAIT_CRD = $('#wait-card');
    const SIGN = $('#signature');
    const SIGN_CRD = $('#sign-card');
    const INP = $('#input');
    const VERIFY = $('#verify');


    RSA_btn.on('click', function(e){
        e.preventDefault();
        $('#mode-remainder').text('Selected mode RSA');
        VERIFY.attr('hidden', '');
        INP.html('');
        mode = 'rsa'
        uri = '/rsa'
        action = '/keys';
        url = host + uri + action;
        
        btn_off(DSA_CHECK_btn);
        btn_off(RSA_CHECK_btn);
        btn_off(DSA_btn);
        btn_on(RSA_btn, url, mode);
    });

    DSA_btn.on('click', function(e){
        e.preventDefault();
        $('#mode-remainder').text('Selected mode DSA');
        VERIFY.attr('hidden', '');
        INP.html('');
        mode = 'dsa'
        uri = '/dsa'
        action = '/keys';
        url = host + uri + action;

        btn_off(DSA_CHECK_btn);
        btn_off(RSA_CHECK_btn);
        btn_off(RSA_btn);
        btn_on(DSA_btn, url, mode);
    });

    RSA_CHECK_btn.on('click', function(e){
        e.preventDefault();
        $('#mode-remainder').text('Selected mode RSA Verification');
        VERIFY.removeAttr('hidden');     
        SIGN.attr('hidden', '');
        uri = '/rsa'
        action = '/verify';
        url = host + uri + action;
        mode = 'rsa_verify';
        btn_off(DSA_CHECK_btn);
        btn_off(DSA_btn);
        btn_off(RSA_btn);
        btn_on(RSA_CHECK_btn);

        WAIT_CRD.text('Input data to ferify the signature')
        let html = '<p>' + b('Verify Signature >>') + '</p>';
        INP.html('');
        html += b('Signature >>')
        html += '<textarea class="form-control verify-data" id="rsa-sign" placeholder="RSA Signature value"></textarea>';
        html += b('Public N value >>')
        html += '<textarea class="form-control verify-data" id="rsa-n" placeholder="RSA Public key N value"></textarea>';
        html += b('Public E value >>')
        html += '<textarea class="form-control verify-data" id="rsa-e" placeholder="RSA Public key E value"></textarea>';
        INP.append(html);
    });

    DSA_CHECK_btn.on('click', function(e){
        e.preventDefault();
        $('#mode-remainder').text('Selected mode DSA Verification');
        VERIFY.removeAttr('hidden');  
        SIGN.attr('hidden', '');    
        uri = '/dsa'
        action = '/verify';
        url = host + uri + action;
        mode = 'dsa_verify';
        

        btn_off(RSA_CHECK_btn);
        btn_off(DSA_btn);
        btn_off(RSA_btn);
        btn_on(DSA_CHECK_btn);

        WAIT_CRD.text('Input data to ferify the signature')
        let html = '<p>' + b('Verify Signature >>') + '</p>';
        INP.html('');
        html += b('R >>')
        html += '<textarea class="form-control verify-data" id="dsa-r" placeholder="DSA Signature R value"></textarea>';
        html += b('S >>')
        html += '<textarea class="form-control verify-data" id="dsa-s" placeholder="DSA Signature S value"></textarea>';
        html += b('G >>')
        html += '<textarea class="form-control verify-data" id="dsa-g" placeholder="DSA Signature G value"></textarea>';
        html += b('P >>')
        html += '<textarea class="form-control verify-data" id="dsa-p" placeholder="DSA Signature P value"></textarea>';
        html += b('Q >>')
        html += '<textarea class="form-control verify-data" id="dsa-q" placeholder="DSA Signature Q value"></textarea>';
        html += b('Public key >>')
        html += '<textarea class="form-control verify-data" id="dsa-public" placeholder="DSA Signature Public key value"></textarea>';
        INP.append(html);
    });

    SIGN.on('click', function(e){
        e.preventDefault();
        action = '/sign';
        url = host + uri + action;
        message = $('#message').val();
        if (keys_ready && message.length){
            let request = {
                message: message,
                private: keys.private
            };
            if (!isEmpty(params)){
                request.params = params;
            }
            $.ajax({
                type: "POST",
                url: url,
                dataType: 'json',
                contentType: "application/json",
                data: JSON.stringify(request),
                success: function (response) {
                    signature = response.signature;
                    SIGN_CRD.removeAttr('hidden');
                    SIGN_CRD.removeClass('bg-danger');
                    SIGN_CRD.addClass('bg-success');
                    let html = b('SIGNATURE');
                    if (mode === 'dsa'){
                        html += b('Keep `k` in secret! K >>') + signature.k;
                        html += b('R >>') + signature.r;
                        html += b('S >>') + signature.s;
                    }
                    else{
                        html += signature;
                    }
                    SIGN_CRD.html(html);
                }
            });
        }

    });

    VERIFY.on('click', function(e){
        e.preventDefault();
        let request = {}
        action = '/verify';

        if (mode === 'dsa_verify'){
            request = {
                message: $('#message').val(),
                signature: {
                    r: $('#dsa-r').val(),
                    s: $('#dsa-s').val()
                },
                params: {
                    g: $('#dsa-g').val(),
                    p: $('#dsa-p').val(),
                    q: $('#dsa-q').val()
                },
                public: $('#dsa-public').val(),
            }
        } else if (mode === 'rsa_verify'){
            request = {
                message: $('#message').val(),
                signature: $('#rsa-sign').val(),
                public: {
                    n: $('#rsa-n').val(),
                    e: $('#rsa-e').val()
                }
            }
        }
        url = host + uri + action;
        SIGN_CRD.removeAttr('hidden');
        $.ajax({
            type: "POST",
            url: url,
            data: JSON.stringify(request),
            dataType: 'json',
            contentType: "application/json",
            success: function (response) {
                SIGN_CRD.removeClass('bg-danger');
                SIGN_CRD.addClass('bg-success');
                SIGN_CRD.html(b(response.status));
                
            },
            error: function(xhr, status, error){
                SIGN_CRD.removeClass('bg-success');
                SIGN_CRD.addClass('bg-danger');
                let html = ''
                console.log();
                if (xhr.status === 500){
                    html += b(xhr.responseJSON.error);
                    html += b('Invalid input. Check the data');
                }
                else if (xhr.status === 400){
                    html += xhr.responseJSON.status;
                }
                SIGN_CRD.html(html);
            }
        });

    })

    function btn_on(btn, url, mode){
        keys_ready = false;
        SIGN.attr('hidden', '');
        SIGN_CRD.attr('hidden', '');
        WAIT_CRD.text('Wait keys from server');
        btn.removeClass('btn-dark');
        btn.addClass('btn-warning')

        if (mode === 'dsa' || mode === 'rsa'){
            $.ajax({
                type: "GET",
                url: url,
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                success: function (response) {
                    keys_ready = true;
                    let html = b('KEEP PRIVATE KEY IN SECRET!<br>Keys:');
                    if (mode === 'rsa'){
                        keys = response;
                        params = {};
                        html += b('PRIVATE:<br/> D >>') + keys.private.d + b(' N >>') + keys.private.n;
                        html += b('PUBLIC: <br/> E >>') + keys.public.e + b(' N >>') + keys.public.n;
                    }
                    else if (mode === 'dsa'){
                        keys = response.keys;
                        params = response.params;
                        html += b('PRIVATE:') + keys.private;
                        html += b('PUBLIC') + keys.public;
                        html += b('<br/>PARAMS:')
                        html += b('    g >>') + params.g;
                        html += b('    p >>') + params.p;
                        html += b('    q >>') + params.q;
                    }
                    WAIT_CRD.html(html);
                    SIGN.removeAttr('hidden');
                }
            });
        }
    }

    
    function btn_off(btn){
        btn.removeClass('btn-warning');
        btn.addClass('btn-dark')
    };

    function b(t){
        return '<br/><b>' + t + '</b><br/>'; 
    };

    function isEmpty(obj) {
        return Object.keys(obj).length === 0;
      }
});

