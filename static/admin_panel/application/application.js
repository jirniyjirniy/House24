$('.form-flat_owner-select').on('change', function () {
    if ($(this).val() === '') {
        $('.form-flat-select').children().remove()
        $.ajax({
            url: `/admin-panel/houses/get-all-flats`,         /* Куда отправить запрос */
            method: 'get',             /* Метод запроса (post или get) */
            dataType: 'html',
            context: 'html',
            success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                $('.form-flat-select').children().remove()
                data = JSON.parse(data);
                var newOption;
                var house_name;
                for (let flat of JSON.parse(data['flats'])) {
                    $.ajax({
                        url: `/admin-panel/houses/get-house-info/${flat['fields']['house']}`,         /* Куда отправить запрос */
                        method: 'get',             /* Метод запроса (post или get) */
                        dataType: 'html',
                        context: 'html',
                        success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                            data = JSON.parse(data)
                            house_name = JSON.parse(data['house'])[0]['fields']['title']
                            newOption = new Option(`${flat['fields']['number']}, ${house_name}`, flat['pk'], false, false);
                            $('.form-flat-select').append(newOption).val([]).trigger('change');
                        }
                    });
                }


            }
        });
    } else {
        let id = $(this).val()
        $.ajax({
            url: `/admin-panel/houses/get-flat-owner/${id}`,         /* Куда отправить запрос */
            method: 'get',             /* Метод запроса (post или get) */
            dataType: 'html',
            context: 'html',
            success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                $('.form-flat-select').children().remove()
                data = JSON.parse(data);
                var newOption;
                var house_name;
                for (let flat of JSON.parse(data['flats'])) {
                    $.ajax({
                        url: `/admin-panel/houses/get-house-info/${flat['fields']['house']}`,         /* Куда отправить запрос */
                        method: 'get',             /* Метод запроса (post или get) */
                        dataType: 'html',
                        context: 'html',
                        success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                            data = JSON.parse(data)
                            house_name = JSON.parse(data['house'])[0]['fields']['title']
                            newOption = new Option(`${flat['fields']['number']}, ${house_name}`, flat['pk'], false, false);
                            $('.form-flat-select').append(newOption).val([]).trigger('change');
                        }
                    });
                }


            }
        });
    }
})
$('html').on('click', '.select2-selection__clear', function () {
    alert('hello')
    $('.form-flat-select').children().remove()
})
