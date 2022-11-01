$('.modal').on('shown.bs.modal', function () {
    $(this).find('[autofocus]').focus();
});

$('.modal').on('hidden.bs.modal', function () {
    $(this).find('form').trigger('reset')
});

function addModel() {
    model_file = document.addModelForm.file.value;
    if (!model_file) {
        document.getElementById('model_file_error').setAttribute('style', 'display: block')
    } else {
        document.getElementById('addModelForm').submit();
    }
}

var input_add_file = document.getElementById('add-file');
var input_edit_file = document.getElementById('edit-file');

input_add_file.onchange = function () {
    model_file = document.addModelForm.file.value;
    if (!model_file) {
        document.getElementById('model_file_error').setAttribute('style', 'display: block')
    } else {
        document.getElementById('model_file_error').setAttribute('style', 'display: none')
    }
};

input_edit_file.onchange = function () {
    model_file = document.editModelForm.file.value;
    if (!model_file) {
        document.getElementById('model_file_error').setAttribute('style', 'display: block')
    } else {
        names = model_file.split('\\')
        $('#name').text(names[names.length - 1]);
        document.getElementById('model_file_error').setAttribute('style', 'display: none')
    }
};

function editModel() {
    model_file = document.editModelForm.file.value;
    if (!model_file) {
        document.getElementById('edit_model_file_error').setAttribute('style', 'display: block')
    } else {
        document.getElementById('editModelForm').submit();
    }
}

function validateEditModel() {
    model_file = document.editModelForm.file.value;

    if (!model_file) {
        document.getElementById('edit_model_file_error').setAttribute('style', 'display: block')
    } else {
        document.getElementById('edit_model_file_error').setAttribute('style', 'display: none')
    }
}

function deleteModel() {
    document.getElementById('deleteModelForm').submit();
}

// Gọi api detail Model
$(document).on('click', '.edit-btn, .delete-btn', function () {
    var model_id = $(this).attr("id");

    $.ajax({
        url: "/model/detail/" + model_id,
        method: "GET",
        success: function (data) {
            $('#edit_id').val(data.data.id);
            $('#delete_id').val(data.data.id);
            $('#name').text(data.data.name);
            $('#delete_name').text(data.data.name);
            $('#status').val(data.data.status == true ? 1 : 0);
        }
    });

});

var errorDisplay = document.querySelectorAll('.dz-error-message');
errorDisplay[errorDisplay.length - 1].innerHTML = 'You can only upload one file at once';