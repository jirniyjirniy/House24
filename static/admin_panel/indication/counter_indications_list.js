$('#filter').on('cancel.daterangepicker', function () {
    $(this).trigger('submit')

});
$('#filter').on('apply.daterangepicker', function () {
    $(this).trigger('submit')

});
if ($('.form-house-select option:selected').val() === '') {
    clearSelects()
} else {
    $.ajax({
        url: `/admin-panel/get-house-info/${$('.form-house-select option:selected').val()}`,
        method: 'get',
        dataType: 'html',
        context: 'html',
        success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
            if ($('.form-section-select option:selected').text() !== '') {
                var selectedSection = $('.form-section-select').val()
            }
            clearSelects()

            let newOption;
            data = JSON.parse(data)
            for (let section of JSON.parse(data['sections'])) {
                newOption = new Option(`${section['fields']['title']}`, section['pk'], false, false);
                $('.form-section-select').append(newOption).val([])

            }
            $('.form-section-select').append(newOption).val(selectedSection)

        }

    });
}

function clearSelects() {
    $('.form-section-select').children().remove()
}
