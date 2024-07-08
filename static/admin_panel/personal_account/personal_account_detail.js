$('body').on('click','.accept_payment',function () {
    if($(this).hasClass('dsbld')){
        alert('Лицевой счет неактивен или не привязан к квартире')
    }else {
    }


})