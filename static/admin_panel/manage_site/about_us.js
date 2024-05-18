let docsTotal = $('#id_docs-TOTAL_FORMS')

$('.add__doc').on('click', function () {
    $(this).before(
        `
        <div class="formset__item">
            <div class="mb-3">
                <div class="d-flex flex-row justify-content-between">
                    <div class="d-flex flex-row align-items-center">
                        <div class="mr-3">
                               <i class="fa fa-file-o fa-3x pull-left" style="width: 32px;" aria-hidden="true"></i>
                        </div>
                        <div>
                            <label class="form-label d-block" for="id_docs-${docsTotal.val()}-file">PDF, JPG (макс. размер 20 Mb)</label>
                            <input type="file" name="docs-${docsTotal.val()}-file"  class="" id="id_docs-${docsTotal.val()}-file">
                        </div>
                    </div>
                     <div>
                        <i class="fa fa-trash text-red delete__doc" aria-hidden="true"></i>
                    </div>
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label" for="id_docs-${docsTotal.val()}-name">Название документа</label>
                <input type="text"  name="docs-${docsTotal.val()}-name" maxlength="100" class="form-control rounded-0 shadow-none" placeholder="Название документа" id="id_docs-${docsTotal.val()}-name">
            </div>
            <input type="hidden" name="docs-${docsTotal.val()}-id" id="id_docs-${docsTotal.val()}-id">
        </div>
        `
    )
    $('.delete__doc').on('click', function () {
        $(this).parent('.formset__item').remove()
    })
    docsTotal.val(Number(docsTotal.val()) +1)
})

$('.delete__d').click(function (){
    return confirm('Вы точно хотите удалить?')
})
