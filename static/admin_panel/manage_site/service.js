let info_photoTotal = $('#id_info_photo-TOTAL_FORMS')

$('.add__service').on('click', function () {
    $('.formset').append(
        `
                <div class="formset__item col-12 col-md-4 p-2 col-12 col-md-4 p-2">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5> Услуга ${Number(info_photoTotal.val()) + 1} </h5>
                        <div class="service__delete">
                            <i class="fa fa-trash text-red " style="cursor: pointer" aria-hidden="true"></i>
                        </div>
                    </div>
                    <img src="https://via.placeholder.com/600.png?text=No+Image" class="img-fluid w-100" style="height: 200px;object-fit: cover" alt="">
                    <div class="mb-3">
                        <label class="control-label mt-2 d-block" for="id_info_photo-${info_photoTotal.val()}-img">Рекомендуемый размер:
                            (650x300)</label>
                        <input type="file" name="info_photo-${info_photoTotal.val()}-img" class="" accept="image/*" id="id_info_photo-${info_photoTotal.val()}-img">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="id_info_photo-${info_photoTotal.val()}-title">Заголовок</label>
                        <input type="text" name="info_photo-${info_photoTotal.val()}-title"  maxLength="100" class="form-control rounded-0 shadow-none" placeholder="Заголовок" id="id_info_photo-${info_photoTotal.val()}-title">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="id_info_photo-${info_photoTotal.val()}-description">Описание</label>
                        <textarea name="info_photo-${info_photoTotal.val()}-description" cols="40" rows="10" class="form-control rounded-0 shadow-none summernote" placeholder="Описание" id="id_info_photo-${info_photoTotal.val()}-description"></textarea>
                    </div>
                    <input type="hidden" name="info_photo-${info_photoTotal.val()}-id"  id="id_info_photo-${info_photoTotal.val()}-id">
                    <div class="mb-3 hidden">
                        <div class="form-check">
                            <input type="checkbox" name="info_photo-${info_photoTotal.val()}-DELETE" class="form-check-input" id="id_info_photo-${info_photoTotal.val()}-DELETE" style="display: none;">
                            <label class="form-check-label" for="id_info_photo-${info_photoTotal.val()}-DELETE" style="display: none;">Удалить</label>
                        </div>
                    </div>
                </div>
        `
    )
    $(document).ready(function () {
        $('.summernote').summernote({
            height: 200,
            lang: 'ru-RU',
        });
    });
    info_photoTotal.val(Number(info_photoTotal.val()) + 1);
})

$('body').on('click', '.service__delete', function () {
    $(this).parents('.formset__item').find('[name$=\'DELETE\']').attr('checked', 'checked')
    $(this).parents('.formset__item').fadeOut('slow', function () {})
})
