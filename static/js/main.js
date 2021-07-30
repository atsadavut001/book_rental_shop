function memberAddCredit() {
    let mb_code = document.getElementById('member_code').value,
        credit = document.getElementById('add_credit').value;

    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'post';
    form.action = `/member/${mb_code}?credit=${credit}`;
    form.submit();
    document.body.removeChild(form);
}

function getMemberID(mb_id) {
    document.getElementById('member_code').value = mb_id;
}

function getBookData(book) {
    document.getElementById('edit_id').value = book.id;
    document.getElementById('edit_name').value = book.name;
    document.getElementById('edit_price').value = book.price;
    document.getElementById('edit_type').value = book.type;
    document.getElementById('edit_num').value = book.num;
}

function editBookById(form_book) {
    var form = form_book;
    form.method = 'post';
    form.action = `/books/${document.getElementById('edit_id').value}`;
    form.submit();

}