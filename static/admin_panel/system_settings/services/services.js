let measureTotal = $('#id_measure_formset-TOTAL_FORMS');

$("[name$='DELETE'], [for$='DELETE']").hide()
$('body').on('click', '.service__delete', function () {
    if ($(this).hasClass('dsbld-service')) {
        alert('Эта услуга используется в квитанциях. Удаление невозможно.')
    } else {
        if (confirm('Удалить?')) {
            $(this).parents('.formset__item').find('[name$=\'DELETE\']').attr('checked', 'checked')
            $(this).parents('.formset__item').fadeOut('slow', function () {

            })
        }
    }
})

$('body').on('click', '.measure__delete', function () {
    if ($(this).hasClass('dsbld')) {
        alert('Эта единица измерения используется в услугах. Удаление невозможно.')
    } else {
        if (confirm('Удалить?')) {
            $(this).parents('.formset__item').find('[name$=\'DELETE\']').attr('checked', 'checked')
            $(this).parents('.formset__item').fadeOut('slow', function () {

            })
        }
    }
})

$('.add__measure').on('click', function () {
    $(this).before(
        `
        <div class="formset__item">
            <div class="mb-3">
                <label class="form-label" for="id_measure_formset-${measureTotal.val()}-title">Ед. изм.</label>
                <div class="input-group">
                    <input type="text" name="measure_formset-${measureTotal.val()}-title"  class="form-control measure__title rounded-0 shadow-none" maxlength="100" placeholder="Ед. изм." id="id_measure_formset-${measureTotal.val()}-title">
                    <span><button type="button" class="btn btn-default h-100 rounded-0 measure__delete"><i class="fa fa-trash" aria-hidden="true"></i></button></span>
                </div>
            </div>
            <input type="hidden" name="measure_formset-${measureTotal.val()}-id" id="id_measure_formset-${measureTotal.val()}-id">
            <div class="mb-3">
                <div class="form-check">
                    <input type="checkbox" name="measure_formset-${measureTotal.val()}-DELETE" class="form-check-input" id="id_measure_formset-${measureTotal.val()}-DELETE" style="display: none;">
                    <label class="form-check-label" for="id_measure_formset-${measureTotal.val()}-DELETE" style="display: none;">Удалить</label>
                </div>
            </div>
        </div>
        `
    )
    measureTotal.val(Number(measureTotal.val()) + 1);
})

let serviceTotal = $('#id_service_formset-TOTAL_FORMS')
$('.add__service').on('click', function () {
    let measureSelect = $('.measure__select')

    $(this).before(
        `
        <div class="formset__item">
            <div class="row mb-2">
                <div class="col-12 col-sm-7">
                    <div class="mb-3">
                        <label class="form-label" for="id_service_formset-${serviceTotal.val()}-title">Услуга</label>
                        <input type="text" name="service_formset-${serviceTotal.val()}-title"  maxlength="100" class="form-control rounded-0 shadow-none" placeholder="Услуга" id="id_service_formset-${serviceTotal.val()}-title">
                    </div>
                </div>
                <div class="col-9 col-sm-4 pe-0">
                    <div class="mb-3">
                        <label class="form-label" for="id_service_formset-${serviceTotal.val()}-measure">Ед. изм.</label>
                        <select name="service_formset-${serviceTotal.val()}-measure" class="form-select rounded-0 shadow-none" id="id_service_formset-${serviceTotal.val()}-measure">
                            <option value="" selected>Выберите...</option>

                        </select>
                    </div>
                </div>
                <div class="col-3 col-sm-1 ps-0">
                    <button type="button" class="btn btn-default rounded-0 service__delete" style="margin-top: 32px;height: 38px;"><i class="fa fa-trash" aria-hidden="true"></i></button>
                </div>
            </div>
            <div class="mb-3">
                <div class="form-check">
                    <input type="checkbox" name="service_formset-${serviceTotal.val()}-show_in_indication" class="form-check-input rounded-0 shadow-none" id="id_service_formset-${serviceTotal.val()}-show_in_indication" checked="">
                    <label class="form-check-label" for="id_service_formset-${serviceTotal.val()}-show_in_indication">Показывать в счетчиках</label>
                </div>
            </div>
            <input type="hidden" name="service_formset-${serviceTotal.val()}-id" id="id_service_formset-${serviceTotal.val()}-id">
            <div class="mb-3">
                <div class="form-check">
                    <input type="checkbox" name="service_formset-${serviceTotal.val()}-DELETE" class="form-check-input" id="id_service_formset-${serviceTotal.val()}-DELETE" style="display: none;">
                    <label class="form-check-label" for="id_service_formset-${serviceTotal.val()}-DELETE" style="display: none;">Удалить</label>
                </div>
            </div>
        </div>
        `
    )
    serviceTotal.val(Number(serviceTotal.val()) + 1);

    id_service_formset-${serviceTotal.val()}-measure
})
