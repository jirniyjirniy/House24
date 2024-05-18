let tariff_serviceTotal = $('#id_tariff_service-TOTAL_FORMS')
$('.add__tariff-service').on('click', function () {
    let serviceSelect = $('.service__select')
    $(this).before(
        `
        <div class="formset__item">
            <div class="row mb-2">
                <div class="col-12 col-md-4 pe-0">
                    <div class="mb-3">
                        <label class="form-label" for="id_tariff_service-${tariff_serviceTotal.val()}-service">Услуга</label>
                        <select name="tariff_service-${tariff_serviceTotal.val()}-service" class="form-select form-service-select rounded-0 shadow-none" id="id_tariff_service-${tariff_serviceTotal.val()}-service">
                            <option value="" selected>Выберите...</option>
                            ${serviceSelect.html()}>
                        </select>
                    </div>
                </div>
                <div class="col-12 col-md-3 pe-0">
                    <div class="mb-3">
                    <label class="form-label" for="id_tariff_service-${tariff_serviceTotal.val()}-price">Цена</label>
                    <input type="text" name="tariff_service-${tariff_serviceTotal.val()}-price" class="form-control rounded-0 shadow-none" placeholder="Price" id="id_tariff_service-${tariff_serviceTotal.val()}-price"></div>
                </div>
                <div class="col-12 col-md-2 pe-0">
                    <div class="mb-3">
                        <label class="form-label" for="id_tariff_service-${tariff_serviceTotal.val()}-currency">Валюта</label>
                        <input type="text" name="tariff_service-${tariff_serviceTotal.val()}-currency" value="грн" disabled="" class="form-control rounded-0 shadow-none" placeholder="грн" id="id_tariff_service-${tariff_serviceTotal.val()}-currency">
                    </div>
                </div>
                <div class="col-12 col-md-2 pe-0">
                    <div class="mb-3">
                        <label class="form-label" for="measure">Ед. изм.</label>
                        <select disabled name="measure" class="form-select rounded-0 shadow-none">
                            <option id="measure" selected></option>
                        </select>
                    </div>
                </div>
                <div class="col-12 col-md-1 ps-0">
                    <button type="button" class="btn btn-default rounded-0 service__delete" style="margin-top: 32px;height: 38px;"><i class="fa fa-trash" aria-hidden="true"></i></button>
                </div>
            </div>
            <input type="hidden" name="tariff_service-${tariff_serviceTotal.val()}-id" id="id_tariff_service-${tariff_serviceTotal.val()}-id">
            <div class="mb-3 d-none">
                <div class="form-check">
                    <input type="checkbox" name="tariff_service-${tariff_serviceTotal.val()}-DELETE" class="form-check-input" id="id_tariff_service-${tariff_serviceTotal.val()}-DELETE" >
                    <label class="form-check-label" for="id_tariff_service-${tariff_serviceTotal.val()}-DELETE">Удалить</label>
                </div>
            </div>
        </div>
        `
    )
    tariff_serviceTotal.val(Number(tariff_serviceTotal.val()) + 1);

})

$("[name$='DELETE'], [for$='DELETE']").hide()
$('body').on('click', '.service__delete', function () {
    if (confirm('Удалить?')) {
        $(this).parents('.formset__item').find('[name$=\'DELETE\']').attr('checked', 'checked')
        $(this).parents('.formset__item').fadeOut('slow', function () {

        })
    }
})

$('body').on('change', '.form-service-select', function () {
    let id = $(this).val();
    let element = $(this);
    $.ajax({
        url: `/admin-panel/get-measure/${id}`,
        method: 'get',
        dataType: 'html',
        context: 'html',
        success: function (data) {
            element.parents('.formset__item').find('#measure').text(JSON.parse(data)['measure'])
        }
    });
})
