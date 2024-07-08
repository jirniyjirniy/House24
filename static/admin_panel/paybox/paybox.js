$('.form-flat_owner-select').on('change', function () {
    if ($(this).val() === '') {
        $('.personal_account-select').children().remove()
        $.ajax({
            url: `/admin-panel/houses/get-all-flats/`,         /* Куда отправить запрос */
            method: 'get',             /* Метод запроса (post или get) */
            dataType: 'html',
            context: 'html',
            success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                $('.personal_account-select').children().remove()
                data = JSON.parse(data);
                var newOption;
                for (let personal_account of JSON.parse(data['all_personal_accounts'])) {
                    newOption = new Option(`${personal_account['fields']['number']}`, personal_account['pk'], false, false);
                    $('.personal_account-select').append(newOption).val([]).trigger('change');

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
                $('.personal_account-select').children().remove()
                data = JSON.parse(data);
                var newOption;
                for (let personal_account of JSON.parse(data['personal_accounts'])) {
                    newOption = new Option(`${personal_account['fields']['number']}`, personal_account['pk'], false, false);
                    $('.personal_account-select').append(newOption).val([]).trigger('change');
                }
            }
        });
    }
})
$('html').on('click', '.select2-selection__clear', function () {
    $('.form-flat-select').children().remove()
})
