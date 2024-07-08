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
            clearSelects()
            data = JSON.parse(data)
            for (let section of JSON.parse(data['sections'])) {
                if (section['pk'] == selectedSection) {
                    $('.form-section-select').append($(`
                            <option value="${section['pk']}" selected>${section['fields']['title']}</option>
                        `))
                } else {
                    $('.form-section-select').append($(`
                            <option value="${section['pk']}" >${section['fields']['title']}</option>
                        `))
                }
            }
            for (let flat of JSON.parse(data['flats'])) {
                $('.form-flat-select').append($(`
                        <option value="${flat['pk']}">${flat['fields']['number']}</option>
                    `))
            }

        }
    });
}
$('.form-house-select').on('change', function () {
    if ($('.form-house-select option:selected').text() === 'Выберите...') {
        clearSelects()
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

    } else {

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


function clearSelects() {
    $('.form-section-select').children().remove()
    $('.form-section-select').append(`
       <option value="">Выберите...</option>
     `)

    $('.form-flat-select').children().remove()
    $('.form-flat-select').append(`
       <option value="">Выберите...</option>
     `)

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