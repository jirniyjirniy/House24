let serviceTotal = $('#id_service-TOTAL_FORMS')
let measureSelect = $('.measure__select')
let serviceSelect = $('.service__select')
$('.add__service').on('click', function () {
    $('#form-receiptservice-rows').append(
        `
            <tr class="form-receiptservice-row">
               <td>
                    <div class="">
                    <select name="service-${serviceTotal.val()}-service" class="form-select form-service-select rounded-0 shadow-none" id="id_service-${serviceTotal.val()}-service">
                      <option value="" selected="">Выберите...</option>
                      ${serviceSelect.html()}>
                    </select>
                    </div>
               </td>
               <td>
                    <div class="">
                        <input type="text" name="service-${serviceTotal.val()}-consumption" placeholder="" class="form-control consumption rounded-0 shadow-none" id="id_service-${serviceTotal.val()}-consumption">
                    </div>
                </td>
               <td>
                   <div class="">
                       <select name="service-${serviceTotal.val()}-measure" class="form-select form-measure-select rounded-0 shadow-none" id="id_service-${serviceTotal.val()}-measure">
                          <option value="" selected="">Выберите...</option>
                          ${measureSelect.html()}>
                        </select>
                    </div>
                </td>
                <td>
                    <div class="">
                        <input type="text" name="service-${serviceTotal.val()}-unit_price" placeholder="" class="form-control unit_price rounded-0 shadow-none" id="id_service-${serviceTotal.val()}-unit_price">
                    </div>
                </td>
                <td>
                    <div class="">
                        <input type="text" name="service-${serviceTotal.val()}-total_service_price" placeholder="" class="form-control total_service_price rounded-0 shadow-none" id="id_service-${serviceTotal.val()}-total_service_price">
                    </div>
                </td>
                <td>
                    <input type="hidden" name="service-${serviceTotal.val()}-id" id="id_service-${serviceTotal.val()}-id">
                    <input type="checkbox" name="service-${serviceTotal.val()}-DELETE" class="form-check-input d-none" id="id_service-${serviceTotal.val()}-DELETE">
                    <button type="button" class="btn btn-default service__delete" title="Удалить услугу"><i class="fa fa-trash" aria-hidden="true"></i></button>
                </td>
            </tr>
        `)
    serviceTotal.val(Number(serviceTotal.val()) + 1);
})
// $("[name$='DELETE'], [for$='DELETE']").hide()

$('body').on('click', '.service__delete', function () {
    if (confirm('Удалить?')) {
        $(this).parents('.form-receiptservice-row').find('[name$=\'DELETE\']').attr('checked', 'checked')
        $(this).parents('.form-receiptservice-row').fadeOut('slow', function () {

        })
        let total_service_price = $(this).parents('.form-receiptservice-row').find('.total_service_price')
        $('.total_price').val(Number(Number($('.total_price').val()) - Number($(total_service_price).val())).toFixed(2))
        $('#price-total').text($('.total_price').val())

    }
})

$('body').on('change', '.consumption', function () {
    let unit_price = $(this).parents('.form-receiptservice-row').find('.unit_price')
    if (Number($(this).val()) && Number(unit_price.val())) {
        $('.total_price').val(0)
        $('#form-receiptservice-rows').children().not('.d-none').each(function () {
            let unit_price = $(this).find('.unit_price')
            let consumption = $(this).find('.consumption')
            let total_service_price = $(this).find('.total_service_price')
            if (Number(unit_price.val()) && Number(consumption.val())) {
                $(total_service_price).val(Number(unit_price.val() * consumption.val()).toFixed(2))
                $('.total_price').val(Number($('.total_price').val()) + Number($(total_service_price).val()))
                $('#price-total').text(Number($('.total_price').val()).toFixed(2))
            }
        })

    }
})
$('body').on('change', '.unit_price', function () {
    let consumption = $(this).parents('.form-receiptservice-row').find('.consumption')
    if (Number($(this).val()) && Number(consumption.val())) {
        $('.total_price').val(0)
        $('#form-receiptservice-rows').children().not('.d-none').each(function () {
            let unit_price = $(this).find('.unit_price')
            let consumption = $(this).find('.consumption')
            let total_service_price = $(this).find('.total_service_price')
            if (Number(unit_price.val()) && Number(consumption.val())) {
                $(total_service_price).val(Number(unit_price.val() * consumption.val()).toFixed(2))
                $('.total_price').val(Number($('.total_price').val()) + Number($(total_service_price).val()))
                $('#price-total').text(Number($('.total_price').val()).toFixed(2))
            }
        })
    }
})


$('.set-tariff-services').on('click', function () {
    if ($('.form-tariff-select option:selected').text() !== 'Выберите...') {
        // $('#form-receiptservice-rows').empty()
        $('#form-receiptservice-rows').each(function () {
            $(this).find('[name$=\'DELETE\'], [for$=\'DELETE\']').attr('checked', 'checked')
            $(this).find('.form-receiptservice-row').addClass('d-none')
        })
        $('.total_price').val(0)
        $('#price-total').text('0.00')
        let id = $('.form-tariff-select option:selected').val()
        $.ajax({
            url: `/admin-panel/houses/get-tariff-info/${id}`,         /* Куда отправить запрос */
            method: 'get',             /* Метод запроса (post или get) */
            dataType: 'html',
            context: 'html',
            success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                data = JSON.parse(data)
                for (let tariff_service of JSON.parse(data['tariff_services'])) {

                    let service_id = tariff_service['fields']['service']
                    let service_unit_price = tariff_service['fields']['price']
                    $.ajax({
                        url: `/admin-panel/houses/get-service-info/${service_id}`,         /* Куда отправить запрос */
                        method: 'get',             /* Метод запроса (post или get) */
                        dataType: 'html',
                        context: 'html',
                        success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                            data = JSON.parse(data)
                            let service_obj = JSON.parse(data['service'])[0]['fields']
                            let clonedServiceSelect = serviceSelect.clone(true);
                            clonedServiceSelect.find(`option[value="${service_id}"]`).attr('selected', true)
                            let clonedMeasureSelect = measureSelect.clone(true);
                            clonedMeasureSelect.find(`option[value="${service_obj['measure']}"]`).attr('selected', true)
                            $('#form-receiptservice-rows').append(`
                                    <tr class="form-receiptservice-row">
                                       <td>
                                            <div class="">
                                            <select name="service-${serviceTotal.val()}-service" class="form-select form-service-select rounded-0 shadow-none" id="id_service-${serviceTotal.val()}-service">
                                              <option value="">Выберите...</option>
                                              ${clonedServiceSelect.html()}>
                                            </select>
                                            </div>
                                       </td>
                                       <td>
                                            <div class="">
                                                <input type="text" name="service-${serviceTotal.val()}-consumption" placeholder="" class="form-control consumption rounded-0 shadow-none" id="id_service-${serviceTotal.val()}-consumption">
                                            </div>
                                        </td>
                                       <td>
                                           <div class="">
                                               <select name="service-${serviceTotal.val()}-measure" class="form-select form-measure-select rounded-0 shadow-none" id="id_service-${serviceTotal.val()}-measure">
                                                  <option value="">Выберите...</option>
                                                  ${clonedMeasureSelect.html()}>
                                                </select>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="">
                                                <input type="text" name="service-${serviceTotal.val()}-unit_price" value="${service_unit_price}" placeholder="" class="form-control unit_price rounded-0 shadow-none" id="id_service-${serviceTotal.val()}-unit_price">
                                            </div>
                                        </td>
                                        <td>
                                            <div class="">
                                                <input type="text" name="service-${serviceTotal.val()}-total_service_price" placeholder="" class="form-control total_service_price rounded-0 shadow-none" id="id_service-${serviceTotal.val()}-total_service_price">
                                            </div>
                                        </td>
                                        <td>
                                            <input type="hidden" name="service-${serviceTotal.val()}-id" id="id_service-${serviceTotal.val()}-id">
                                            <input type="checkbox" name="service-${serviceTotal.val()}-DELETE" class="form-check-input d-none" id="id_service-${serviceTotal.val()}-DELETE">
                                            <button type="button" class="btn btn-default service__delete" title="Удалить услугу"><i class="fa fa-trash" aria-hidden="true"></i></button>
                                        </td>
                                    </tr>
                            `)
                            serviceTotal.val(Number(serviceTotal.val()) + 1);

                        }
                    });
                }

            }
        });
    } else {
        alert('Тариф не выбран')
    }
})

$('.add-counters').on('click', function () {
    if ($('.form-flat-select').val()) {
        let flat_id = $('.form-flat-select').val()
        let rows = $('#form-receiptservice-rows').children().not('.d-none')
        rows.each(function () {
            let service_id = $(this).find('.form-service-select').val();
            let row = $(this)
            $.ajax({
                url: `/admin-panel/houses/get-indication-info/${flat_id}/${service_id}`,         /* Куда отправить запрос */
                method: 'get',             /* Метод запроса (post или get) */
                dataType: 'html',
                context: 'html',
                success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                    data = JSON.parse(data)
                    try {
                        var indication_obj = jQuery.parseJSON(data['indication']);
                        row.find('.consumption').val(Number(indication_obj[indication_obj.length - 1]['fields']['indication_val']).toFixed(2)).trigger('change')
                        // JSON parsing was successful, do something with jsonObj
                    } catch (e) {
                        // Error occurred during parse, consider it undefined
                        console.log('JSON parse undefined:', e);

                    }
                }
            });
        })
    } else {
        alert('Укажите квартиру')
    }
})
