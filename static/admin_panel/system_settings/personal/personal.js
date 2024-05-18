$('body').on('click', '#showPassword', function(){
    $(this).replaceWith(`
        <button class="btn btn-primary rounded-0" id="hidePassword" type="button" style="height: 38px">
            <i class="fa fa-eye-slash" aria-hidden="true"></i>
        </button>
    `)
    $('.password1').attr('type', 'text')
    $('.password2').attr('type', 'text')
})

$('body').on('click', '#hidePassword', function(){
    $(this).replaceWith(`
        <button class="btn btn-primary rounded-0" id="showPassword" type="button" style="height: 38px">
            <i class="fa fa-eye" aria-hidden="true"></i>
        </button>
    `)
    $('.password1').attr('type', 'password')
    $('.password2').attr('type', 'password')
})

function createPassword(){
    let chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    let string_length = 8;
    let randomstring = '';
    for (let i = 0; i < string_length; i++) {
        let rnum = Math.floor(Math.random() * chars.length);
        randomstring += chars.substring(rnum, rnum+1);
    }
    return randomstring;
}

$('#generatePassword').on('click', function () {
    let password = createPassword();
    $('.password1').val(password).trigger('change');
    $('.password2').val(password).trigger('change');
})
