$(document).ready(function() {
    $('#myTable').DataTable({
        pageLength: 15
    });
});

function validateNumber(event) {
    if (event.key === " " || event.keyCode === 32) {
        event.preventDefault();
    }

    const value = event.target.value;
    event.target.value = value.replace(/[^0-9.]/g, '');
}

function preventSpace(event) {
    if (event.key === " " || event.keyCode === 32) {
      event.preventDefault();
    }
}