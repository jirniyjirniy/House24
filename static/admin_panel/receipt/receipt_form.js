if ($('.form-house-select option:selected').text() === 'Выберите...') {
    clearSelects()
} else {
    $.ajax({
        url: `/admin-panel/houses/get-house-info/${$('.form-house-select option:selected').val()}`,         /* Куда отправить запрос */
        method: 'get',             /* Метод запроса (post или get) */
        dataType: 'html',
        context: 'html',
        success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
            if ($('.form-section-select option:selected').text() !== 'Выберите...') {
                var selectedSection = $('.form-section-select option:selected').val()
            }
            if ($('.form-flat-select option:selected').text() !== 'Выберите...') {
                var selectedFlat = $('.form-flat-select option:selected').val()
            }
            clearSelects()
            data = JSON.parse(data)
            for (let flat of JSON.parse(data['flats'])) {
                if (flat['pk'] == selectedFlat) {
                    $('.form-flat-select').append($(`
                            <option value="${flat['pk']}" selected>${flat['fields']['number']}</option>
                        `))
                    $.ajax({
                        url: `/admin-panel/houses/get-flat-info/${flat['pk']}`,         /* Куда отправить запрос */
                        method: 'get',             /* Метод запроса (post или get) */
                        dataType: 'html',
                        context: 'html',
                        success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                            data = JSON.parse(data)

                            let flat_owner_pk = jQuery.parseJSON(data['flat_owner'])[0]['pk'];
                            let flat_owner_obj = jQuery.parseJSON(data['flat_owner'])[0]['fields'];
                            let user_obj = JSON.parse(data['user'])[0]['fields']
                            $('#user-fullname').empty().append(`<a href="/admin/clients/detail/${flat_owner_pk}">${user_obj['last_name']} ${user_obj['first_name']} ${flat_owner_obj['patronymic']}</a>`)
                            $('#user-phone').empty().append(`<a href="tel:${user_obj['phone']}">${user_obj['phone']}</a>`)


                        }
                    });
                } else {
                    $('.form-flat-select').append($(`
                            <option value="${flat['pk']}" >${flat['fields']['number']}</option>
                        `))
                }
            }
            for (let section of JSON.parse(data['sections'])) {
                if (section['pk'] == selectedSection) {
                    $('.form-section-select').append($(`
                            <option value="${section['pk']}" selected>${section['fields']['title']}</option>
                        `))
                    $.ajax({
                        url: `/admin-panel/houses/get-section-info/${section['pk']}`,         /* Куда отправить запрос */
                        method: 'get',             /* Метод запроса (post или get) */
                        dataType: 'html',
                        context: 'html',
                        success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                            if ($('.form-flat-select option:selected').text() !== 'Выберите...') {
                                var selectedFlat = $('.form-flat-select option:selected').val()
                            }
                            $('.form-flat-select').children().remove()
                            $('.form-flat-select').append(`
                                   <option value="">Выберите...</option>
                                 `)
                            data = JSON.parse(data)
                            for (let flat of JSON.parse(data['flats'])) {
                                if (flat['pk'] == selectedFlat) {
                                    $('.form-flat-select').append($(`
                                            <option value="${flat['pk']}" selected>${flat['fields']['number']}</option>
                                        `))
                                    $.ajax({
                                        url: `/admin-panel/houses/get-flat-info/${flat['pk']}`,         /* Куда отправить запрос */
                                        method: 'get',             /* Метод запроса (post или get) */
                                        dataType: 'html',
                                        context: 'html',
                                        success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                                            data = JSON.parse(data)

                                            let personal_account_obj = jQuery.parseJSON(data['personal_account'])[0]['fields'];
                                            $('.personal_account').val(personal_account_obj['number'])

                                            let flat_owner_pk = jQuery.parseJSON(data['flat_owner'])[0]['pk'];
                                            let flat_owner_obj = jQuery.parseJSON(data['flat_owner'])[0]['fields'];
                                            let user_obj = JSON.parse(data['user'])[0]['fields']
                                            $('#user-fullname').empty().append(`<a href="/admin/clients/detail/${flat_owner_pk}">${user_obj['last_name']} ${user_obj['first_name']} ${flat_owner_obj['patronymic']}</a>`)
                                            $('#user-phone').empty().append(`<a href="tel:${user_obj['phone']}">${user_obj['phone']}</a>`)


                                        }
                                    });
                                } else {
                                    $('.form-flat-select').append($(`
                                            <option value="${flat['pk']}" >${flat['fields']['number']}</option>
                                        `))
                                }
                            }


                        }
                    });
                } else {
                    $('.form-section-select').append($(`
                            <option value="${section['pk']}" >${section['fields']['title']}</option>
                        `))
                }
            }
        }
    });
}
$('.form-house-select').on('change', function () {
    if ($('.form-house-select option:selected').text() === 'Выберите...') {
        clearSelects()
        $('.personal_account').val('')
        $('.form-tariff-select option:selected').removeAttr('selected')
        $(`.form-tariff-select option[value=""]`).attr('selected', true)
    } else {
        let id = $(this).val()
        $.ajax({
            url: `/admin-panel/houses/get-house-info/${id}`,         /* Куда отправить запрос */
            method: 'get',             /* Метод запроса (post или get) */
            dataType: 'html',
            context: 'html',
            success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                clearSelects()
                data = JSON.parse(data)
                for (let section of JSON.parse(data['sections'])) {
                    $('.form-section-select').append($(`
                        <option value="${section['pk']}">${section['fields']['title']}</option>
                    `))
                }
                for (let flat of JSON.parse(data['flats'])) {
                    $('.form-flat-select').append($(`
                        <option value="${flat['pk']}">${flat['fields']['number']}</option>
                    `))
                }

            }
        });
    }
})
$('.form-section-select').on('change', function () {
    if ($('.form-section-select option:selected').text() === 'Выберите...') {
        $('.form-flat-select').children().remove()
        $('.form-flat-select').append(`
           <option value="">Выберите...</option>
         `)
        $.ajax({
            url: `/admin-panel/houses/get-house-info/${$('.form-house-select option:selected').val()}`,         /* Куда отправить запрос */
            method: 'get',             /* Метод запроса (post или get) */
            dataType: 'html',
            context: 'html',
            success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                data = JSON.parse(data)
                for (let flat of JSON.parse(data['flats'])) {
                    $('.form-flat-select').append($(`
                        <option value="${flat['pk']}">${flat['fields']['number']}</option>
                    `))
                }
            }
        });
        $('.personal_account').val('')
        $('.form-tariff-select option:selected').removeAttr('selected')
        $(`.form-tariff-select option[value=""]`).attr('selected', true)
        $('#user-fullname').text('не выбран')
        $('#user-phone').text('не выбран')
    } else {
        $('#user-fullname').text('не выбран')
        $('#user-phone').text('не выбран')
        let id = $(this).val()
        $.ajax({
            url: `/admin-panel/houses/get-section-info/${id}`,         /* Куда отправить запрос */
            method: 'get',             /* Метод запроса (post или get) */
            dataType: 'html',
            context: 'html',
            success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                $('.form-flat-select').children().remove()
                $('.form-flat-select').append(`
                   <option value="">Выберите...</option>
                 `)
                data = JSON.parse(data)
                for (let flat of JSON.parse(data['flats'])) {
                    $('.form-flat-select').append($(`
                        <option value="${flat['pk']}">${flat['fields']['number']}</option>
                    `))
                }

            }
        });

    }
})
$('.form-flat-select').on('change', function () {
    if ($('.form-flat-select option:selected').text() === 'Выберите...') {
        $('#user-fullname').text('не выбран')
        $('#user-phone').text('не выбран')
        $('.personal_account').val('')
        $('.form-tariff-select option:selected').removeAttr('selected')
        $(`.form-tariff-select option[value=""]`).attr('selected', true)

    } else {
        $('#user-fullname').text('не выбран')
        $('#user-phone').text('не выбран')
        $('.personal_account').val('')
        $('.form-tariff-select option:selected').removeAttr('selected')
        $(`.form-tariff-select option[value=""]`).attr('selected', true)
        let id = $(this).val()
        $.ajax({
            url: `/admin-panel/houses/get-flat-info/${id}`,         /* Куда отправить запрос */
            method: 'get',             /* Метод запроса (post или get) */
            dataType: 'html',
            context: 'html',
            success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                data = JSON.parse(data)
                try {
                    let flat_owner_pk = jQuery.parseJSON(data['flat_owner'])[0]['pk'];
                    let flat_owner_obj = jQuery.parseJSON(data['flat_owner'])[0]['fields'];
                    let user_obj = JSON.parse(data['user'])[0]['fields']
                    $('#user-fullname').empty().append(`<a href="/admin-panel/clients/detail/${flat_owner_pk}">${user_obj['last_name']} ${user_obj['first_name']} ${flat_owner_obj['patronymic']}</a>`)
                    $('#user-phone').empty().append(`<a href="tel:${user_obj['phone']}">${user_obj['phone']}</a>`)
                } catch (e) {
                    // Error occurred during parse, consider it undefined
                    console.log('JSON parse undefined:', e);

                }
                try {
                    let personal_account_obj = jQuery.parseJSON(data['personal_account'])[0]['fields'];
                    $('.personal_account').val(personal_account_obj['number'])

                } catch (e) {
                    // Error occurred during parse, consider it undefined
                    console.log('JSON parse undefined:', e);

                }
                try {
                    let tariff_obj = jQuery.parseJSON(data['tariff'])[0];
                    $('.form-tariff-select option:selected').removeAttr('selected')
                    $(`.form-tariff-select option[value="${tariff_obj['pk']}"]`).attr('selected', true)
                    $("#receipt-form").validate().element("#id_tariff");

                } catch (e) {
                    // Error occurred during parse, consider it undefined
                    console.log('JSON parse undefined:', e);

                }
            }
        });
        $.ajax({
            url: `/admin-panel/houses/get-indication-sorted-list/${id}`,         /* Куда отправить запрос */
            method: 'get',             /* Метод запроса (post или get) */
            dataType: 'html',
            context: 'html',
            success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                $('.indications-table').html(data)
            }
        });


    }
})

function clearSelects() {
    $('.form-section-select').children().remove()
    $('.form-section-select').append(`
       <option value="">Выберите...</option>
     `)
    $('.form-flat-select').children().remove()
    $('.form-flat-select').append(`
       <option value="">Выберите...</option>
     `)
    $('#user-fullname').text('не выбран')
    $('#user-phone').text('не выбран')
}

$('.number').attr('value', generateNumber())

function generateNumber() {
    var chars = "0123456789";
    var string_length = 5;
    var randomstring1 = '';
    var randomstring2 = '';
    for (var i = 0; i < string_length; i++) {
        var rnum = Math.floor(Math.random() * chars.length);
        randomstring1 += chars.substring(rnum, rnum + 1);
    }
    for (var i = 0; i < string_length; i++) {
        var rnum = Math.floor(Math.random() * chars.length);
        randomstring2 += chars.substring(rnum, rnum + 1);
    }
    let result = randomstring1 + '-' + randomstring2
    return result;
}
