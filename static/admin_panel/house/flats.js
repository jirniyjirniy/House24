$('#filter').on('change', function () {
    $(this).trigger('submit')
});


if ($('.form-house-select option:selected').val() === '') {
    clearSelects()
} else {
    $.ajax({
        url: `/admin-panel/get-house-info/${$('.form-house-select option:selected').val()}`,         /* Куда отправить запрос */
        method: 'get',             /* Метод запроса (post или get) */
        dataType: 'html',
        context: 'html',
        success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
            if ($('.form-section-select option:selected').text() !== '') {
                var selectedSection = $('.form-section-select').val()
            }
            if ($('.form-floor-select option:selected').text() !== '') {
                var selectedFloor = $('.form-floor-select').val()
            }
            clearSelects()

            let newOption;
            data = JSON.parse(data)
            for (let section of JSON.parse(data['sections'])) {
                newOption = new Option(`${section['fields']['title']}`, section['pk'], false, false);
                $('.form-section-select').append(newOption).val([])

            }
            $('.form-section-select').append(newOption).val(selectedSection)


            for (let floor of JSON.parse(data['floors'])) {
                newOption = new Option(`${floor['fields']['title']}`, floor['pk'], false, false);
                $('.form-floor-select').append(newOption).val([])
            }
            $('.form-floor-select').append(newOption).val(selectedFloor)


        }

    });
}

function clearSelects() {
    $('.form-section-select').children().remove()
    $('.form-floor-select').children().remove()
}
