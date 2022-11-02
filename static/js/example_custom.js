$('.modal').on('shown.bs.modal', function () {
    $(this).find('[autofocus]').focus();
});

$('.modal').on('hidden.bs.modal', function () {
    $(this).find('form').trigger('reset')
});

function addExample() {
    example_file = document.addExampleForm.file.value;
    if (!example_file) {
        document.getElementById('example_file_error').setAttribute('style', 'display: block')
    } else {
        document.getElementById('addExampleForm').submit();
    }
}

function validateExample() {
    example_file = document.addExampleForm.file.value;

    if (!example_file) {
        document.getElementById('example_file_error').setAttribute('style', 'display: block')
    } else {
        document.getElementById('example_file_error').setAttribute('style', 'display: none')
    }
}

function editExample() {
    example_file = document.editExampleForm.file.value;
    if (!example_file) {
        document.getElementById('edit_example_file_error').setAttribute('style', 'display: block')
    } else {
        document.getElementById('editExampleForm').submit();
    }
}

function validateEditExample() {
    example_file = document.editExampleForm.file.value;

    if (!example_file) {
        document.getElementById('edit_example_file_error').setAttribute('style', 'display: block')
    } else {
        document.getElementById('edit_example_file_error').setAttribute('style', 'display: none')
    }
}

function deleteExample() {
    document.getElementById('deleteExampleForm').submit();
}

// Gọi api detail example
$(document).on('click', '.edit-btn, .delete-btn', function () {
    var example_id = $(this).attr("id");

    $.ajax({
        url: "/example/detail/" + example_id,
        method: "GET",
        success: function (data) {
            $('#edit_id').val(data.data.id);
            $('#delete_id').val(data.data.id);
            $('#name').val(data.data.name);
            $('#delete_name').text(data.data.name);
            $('#status').val(data.data.status == true ? 1 : 0);
            $('#example_name').text(data.data.name);
        }
    });

});