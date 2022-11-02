$('.modal').on('shown.bs.modal', function () {
    $(this).find('[autofocus]').focus();
});

$('.modal').on('hidden.bs.modal', function () {
    $(this).find('form').trigger('reset')
});

function addLabel() {
    label_name = document.addLabelForm.name.value;
    if (!label_name) {
        document.getElementById('label_name_error').setAttribute('style', 'display: block')
    } else {
        document.getElementById('addLabelForm').submit();
    }
}

function validateLabel() {
    label_name = document.addLabelForm.name.value;

    if (!label_name) {
        document.getElementById('label_name_error').setAttribute('style', 'display: block')
    } else {
        document.getElementById('label_name_error').setAttribute('style', 'display: none')
    }
}

function editLabel() {
    label_name = document.editLabelForm.name.value;
    if (!label_name) {
        document.getElementById('edit_label_name_error').setAttribute('style', 'display: block')
    } else {
        document.getElementById('editLabelForm').submit();
    }
}

function validateEditLabel() {
    label_name = document.editLabelForm.name.value;

    if (!label_name) {
        document.getElementById('edit_label_name_error').setAttribute('style', 'display: block')
    } else {
        document.getElementById('edit_label_name_error').setAttribute('style', 'display: none')
    }
}

function deleteLabel() {
    document.getElementById('deleteLabelForm').submit();
}

// Gọi api detail label
$(document).on('click', '.edit-btn, .delete-btn', function () {
    var label_id = $(this).attr("id");

    $.ajax({
        url: "/label/detail/" + label_id,
        method: "GET",
        success: function (data) {
            $('#edit_id').val(data.data.id);
            $('#delete_id').val(data.data.id);
            $('#name').val(data.data.name);
            $('#delete_name').text(data.data.name);
            $('#status').val(data.data.status == true ? 1 : 0);
        }
    });

});