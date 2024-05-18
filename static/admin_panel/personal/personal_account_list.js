$('filter').on('change', function () {
    $(this).trigger('submit')
})

if ($('.form-house-select option:selected').text() === ''){
}else {
    $.ajax({
        url: `/houses/get-house-info/${$('.form-house-select option:selected').val()}`,
        method: 'get',
        dataType: 'html',
        context: 'html',
        success: function (data) {
            data = JSON.parse(data)
            for (let section of JSON.parse(data['sections'])){
                $('.form-section-select').append($(`
                <option value="${section['pk']}">${section['fields']['title']}</option>`))
            }
        }
    });
}


if($('.form-house-select option:selected').val() === ''){
    clearSelects()
}else{
    $.ajax({
        url: `/houses/get-house-info/${$('.form-house-selectoption:selected').val()}`,
        method: 'get',
        dataType: 'html',
        context: 'html',
        success: function (data) {
            if ($('.form-house-select option:selected').text() === ''){
                var selectedSection = $('.form-house-select').val();
            }
            clearSelects()

            let newOption;
            data = JSON.parse(data)
            for(let section of JSON.parse(data['sections'])){
                newOption = new Option(`${section['fields']['title']}`, section['pk'], false, false);
                $('.form-section-select').append(newOption).val([]);
            }

            $('.form-section-select').append(newOption).val(selectedSection);
        }
    })
}

function clearSelects() {
    $('.form-section-select').children().remove()
}