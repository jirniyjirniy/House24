$('body').on('click','#showPass',function () {
    $(this).replaceWith(`
     <button type="button" class="btn btn-primary rounded-0" style="height: 38px" id="hidePass">
        <i class="fa fa-eye-slash" aria-hidden="true"></i>
     </button>
    `)
    $('.password1').attr('type','text')
    $('.password2').attr('type','text')
})

$('body').on('click','#hidePass',function () {
    $(this).replaceWith(`
     <button type="button" class="btn btn-primary rounded-0" style="height: 38px" id="showPass">
        <i class="fa fa-eye" aria-hidden="true"></i>
     </button>
    `)
    $('.password1').attr('type','password')
    $('.password2').attr('type','password')
})
function generatePassword() {
    var chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    var string_length = 8;
    var randomstring = '';
    for (var i=0; i<string_length; i++) {
        var rnum = Math.floor(Math.random() * chars.length);
        randomstring += chars.substring(rnum,rnum+1);
    }
    return randomstring;
}

$("#generatePass").click(function() {
    var password = generatePassword();
    $(".password1").val(password).trigger('change');
    $(".password2").val(password).trigger('change');
});