if ($('.form-house-select option:selected').text() === 'Выберите...') {
    clearSelects()
} else {

    $.ajax({
        url: `/admin-panel/houses/get-house-info/${$('.form-house-select option:selected').val()}/`, /* Куда отправить запрос */
        method: 'get',             /* Метод запроса (post или get) */
        dataType: 'html',
        context: 'html',
        success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
            if ($('.form-section-select option:selected').text() !== 'Выберите...') {
                var selectedSection = $('.form-section-select option:selected').val()
            }
            if ($('.form-floor-select option:selected').text() !== 'Выберите...') {
                var selectedFloor = $('.form-floor-select option:selected').val()
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
            for (let floor of JSON.parse(data['floors'])) {
                if (floor['pk'] == selectedFloor) {
                    $('.form-floor-select').append($(`
                            <option value="${floor['pk']}" selected>${floor['fields']['title']}</option>
                        `))
                } else {
                    $('.form-floor-select').append($(`
                            <option value="${floor['pk']}">${floor['fields']['title']}</option>
                        `))
                }
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
            url: `/admin-panel/houses/get-house-info/${id}/`,         /* Куда отправить запрос */
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
                for (let floor of JSON.parse(data['floors'])) {
                    $('.form-floor-select').append($(`
                        <option value="${floor['pk']}">${floor['fields']['title']}</option>
                    `))
                }
            }
        });
    }
})

function clearSelects() {
    $('.form-section-select').children().remove()
    $('.form-floor-select').children().remove()
    $('.form-section-select').append(`
       <option value="">Выберите...</option>
     `)
    $('.form-floor-select').append(`
       <option value="">Выберите...</option>
     `)
}


$('.personal_account-select').select2({
    placeholder: {
        id: "",
        text: "или выберите из списка..." //Should be text not placeholder
    },
    allowClear: true,

})
// $('.personal_account-select').on
//Set the default placeholder
var defaultPlaceholder = $('.personal_account-select').attr('placeholder');
$('#select2-my-select2-container .select2-selection__rendered').html(defaultPlaceholder);

//Update the placeholder when a selection is made
$('#my-select2').on('change', function () {
    var selectedValue = $('#my-select2').val();
    if (selectedValue) {
        $('#select2-my-select2-container .select2-selection__rendered').html(selectedValue);
    } else {
        $('#select2-my-select2-container .select2-selection__rendered').html(defaultPlaceholder);
    }
});


$('.personal_account-select').val("").trigger("change");
$('.personal_account-res').parent().removeClass('mb-3')
$('.personal_account-select').on('change', function () {
    if ($('.personal_account-select option:selected').text() === 'или выберите из списка...') {
    } else {
        $('.personal_account-res').val($('.personal_account-select option:selected').text())
        $(this).val("").trigger("change");

    }
})
