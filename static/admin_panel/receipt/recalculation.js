$('.total_price').val(0)
$('#form-receiptservice-rows').children().each(function () {
    let unit_price = $(this).find('.unit_price')
    let consumption = $(this).find('.consumption')
    let total_service_price = $(this).find('.total_service_price')
     if (Number(unit_price.val()) && Number(consumption.val())) {
         $(total_service_price).val(Number(unit_price.val()*consumption.val()).toFixed(2))
         $('.total_price').val(Number($('.total_price').val())+Number($(total_service_price).val()))
         $('#price-total').text(Number($('.total_price').val()).toFixed(2))
     }
})
