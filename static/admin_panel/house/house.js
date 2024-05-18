let sectionTotal = $('#id_section-TOTAL_FORMS');

$("[name$='DELETE'], [for$='DELETE']").hide();

$('body').on('click', '.section__delete', function () {
    if (confirm('Удалить?')) {
        $(this).parents('.formset__item').find('[name$=\'DELETE\']').attr('checked', 'checked');
        $(this).parents('.formset__item').fadeOut('slow', function () {
        })
    }
})

$('.add__section').on('click', function () {
    $(this).before(
        `
        <div class="formset__item text-left">
            <div class="mb-3 row">
                <div class="col-9 col-sm-11 pe-0">
                    <label class="form-label" for="id_section-${sectionTotal.val()}-title">Название</label>
                    <input type="text" name="section-${sectionTotal.val()}-title" placeholder="" value="Секция ${Number(sectionTotal.val()) + 1}" maxlength="100" class="form-control rounded-0 shadow-none" id="id_section-${sectionTotal.val()}-title">
                </div>
                <div class="col-3 col-sm-1 pe-0 ps-0" style="height: 38px;margin-top: 32px;">
                    <button type="button" class="btn btn-default h-100 rounded-0 section__delete bg-danger"><i class="fa fa-trash" aria-hidden="true"></i></button>
                </div>
            </div>
            <input type="hidden" name="section-${sectionTotal.val()}-id" id="id_section-${sectionTotal.val()}-id">
            <div class="mb-3">
                <div class="form-check">
                    <input type="checkbox" name="section-${sectionTotal.val()}-DELETE" class="form-check-input" id="id_section-${sectionTotal.val()}-DELETE" style="display: none;">
                    <label class="form-check-label" for="id_section-${sectionTotal.val()}-DELETE" style="display: none;">Delete</label>
                </div>
            </div>
        </div>
        `
    )
    sectionTotal.val(Number(sectionTotal.val()) + 1);
})

let floorTotal = $('#id_floor-TOTAL_FORMS')

$('body').on('click', 'floor__delete', function () {
    if (confirm('Удалить?')) {
        $(this).parents('.formset__item').find('[name$=\'DELETE\']').attr('checked', 'checked');
        $(this).parents('.formset__item').fadeOut('slow', function () {
        })
    }
})

$('.add__floor').on('click', function () {
    $(this).before(
        `
        <div class="formset__item text-left">
            <div class="mb-3 row">
                <div class="col-9 col-sm-11 pe-0">
                    <label class="form-label" for="id_floor-${floorTotal.val()}-title">Название</label>
                    <input type="text" name="floor-${floorTotal.val()}-title" placeholder="" value="Этаж ${Number(floorTotal.val()) + 1}" maxlength="100" class="form-control rounded-0 shadow-none" id="id_floor-${floorTotal.val()}-title">
                </div>
                <div class="col-3 col-sm-1 pe-0 ps-0" style="height: 38px;margin-top: 32px;">
                    <button type="button" class="btn btn-default h-100 rounded-0 floor__delete bg-danger"><i class="fa fa-trash" aria-hidden="true"></i></button>
                </div>
            </div>
            <input type="hidden" name="floor-${floorTotal.val()}-id" id="id_floor-${floorTotal.val()}-id">
            <div class="mb-3">
                <div class="form-check">
                    <input type="checkbox" name="floor-${floorTotal.val()}-DELETE" class="form-check-input" id="id_floor-${floorTotal.val()}-DELETE" style="display: none;">
                    <label class="form-check-label" for="id_floor-${floorTotal.val()}-DELETE" style="display: none;">Delete</label>
                </div>
            </div>
        </div>
        `
    )
    floorTotal.val(Number(floorTotal.val()) + 1);

})

let personalTotal = $('#id_personal-TOTAL_FORMS')


$('body').on('click', '.personal__delete', function () {
    if (confirm('Удалить?')) {
        $(this).parents('.formset__item').find('[name$=\'DELETE\']').attr('checked', 'checked')
        $(this).parents('.formset__item').fadeOut('slow', function () {

        })
    }
})

$('.add__personal').on('click', function () {
    let personalSelect = $('.personal__select').children().first()
    $(this).before(
        `
        <div class="formset__item text-left">
            <div class="row">
                <div class="col-12 col-sm-8 col-md-7 pe-0">
                     <label class="form-label" for="id_personal-${personalTotal.val()}-user">ФИО</label>
                    <select name="personal-${personalTotal.val()}-user" class="form-select form-role-select rounded-0 shadow-none" id="id_personal-${personalTotal.val()}-user">
                        ${personalSelect.html()}
                    </select>
                </div>
               <div class="col-10 col-sm-3 col-md-4 pe-0">
                    <div class="mb-3">
                        <label class="form-label" for="role">Роль</label>
                        <select disabled name="role" class="form-select rounded-0 shadow-none">
                            <option id="role" selected></option>
                        </select>
                    </div>
                </div>
                <div class="col-2 col-sm-1 col-md-1 ps-0">
                    <button type="button" class="btn btn-default rounded-0 personal__delete bg-danger" style="margin-top: 32px;height: 38px;"><i class="fa fa-trash" aria-hidden="true"></i></button>
                </div>
            </div>
            <input type="hidden" name="personal-${personalTotal.val()}-id" id="id_personal-${personalTotal.val()}-id">
            <div class="">
                <div class="form-check">
                    <input type="checkbox" name="personal-${personalTotal.val()}-DELETE" class="form-check-input" id="id_personal-${personalTotal.val()}-DELETE" style="display: none;">
                    <label class="form-check-label" for="id_personal-${personalTotal.val()}-DELETE" style="display: none;">Delete</label>
                </div>
            </div>
        </div>
        `
    )
    personalTotal.val(Number(personalTotal.val()) + 1);

})

$('.form-role-select').each(function () {
    let id = $(this).val()
    let element = $(this)
    $.ajax({
        url: `/admin-panel/get-role/${id}/`,
        method: 'get',
        dataType: 'html',
        context: 'html',
        success: function (data) {
            element.parents('.formset__item').find('#role').text(JSON.parse(data)['role'])
        }
    })
})

$('body').on('change', '.form-role-select', function () {
    let id = $(this).val()
    let element = $(this)
    // JSON.parse(data)['measure']
    $.ajax({
        url: `/admin-panel/get-role/${id}/`,
        method: 'get',
        dataType: 'html',
        context: 'html',
        success: function (data) {
            element.parents('.formset__item').find('#role').text(JSON.parse(data)['role'])
        }
    });
})
