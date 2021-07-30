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

function runShowMembers(members) {
    members_tag = ``;
    for (let i = 0; i < members.length; i++) {
        members_tag += `
        <div class="row mt-3">
            <div class="col-3">
                <p class="mt-1">${members[i].code} : ${members[i].name}</p>
            </div>
            <div class="col-9">
                <button class="btn btn-outline-dark" onclick="selectMemberRent({id:'${members[i].id}', code:'${members[i].code}'})" data-dismiss="modal">Select</button>
            </div>
        </div>     
        `;
    }
    document.getElementById("select_members").innerHTML = members_tag.toString();
}

function searchMemberRent(members) {
    members_tag = ``;
    let code = document.getElementById("search_select_members").value;
    for (let i = 0; i < members.length; i++) {
        let data_code = members[i].code.toLowerCase();
        if (data_code.includes(code.toLowerCase())) {
            members_tag += `
            <div class="row mt-3">
                <div class="col-3">
                    <p class="mt-1">${members[i].code} : ${members[i].name}</p>
                </div>
                <div class="col-9">
                    <button class="btn btn-outline-dark" onclick="selectMemberRent({id:'${members[i].id}', code:'${members[i].code}'})" data-dismiss="modal">Select</button>
                </div>
            </div>     
            `;
        }
    }
    document.getElementById("select_members").innerHTML = members_tag.toString();
}

function selectMemberRent(member) {
    document.getElementById("rent_member_id").value = member.id;
    document.getElementById("rent_member_code").value = member.code;
}

function runShowBooks(books) {
    books_tag = ``;
    for (let i = 0; i < books.length; i++) {
        books_tag += `
        <div class="row mt-3">
            <div class="col-3">
                <p class="mt-1">${books[i].id} : ${books[i].name} : ${books[i].price}$</p>
            </div>
            <div class="col-9">
                <button class="btn btn-outline-dark" onclick="selectBookRent({id:'${books[i].id}', name:'${books[i].name}', price:'${books[i].price}'})" data-dismiss="modal">Select</button>
            </div>
        </div>     
        `;
    }
    document.getElementById("select_books").innerHTML = books_tag.toString();
}

function searchBookRent(books) {
    books_tag = ``;
    let name = document.getElementById("search_select_book").value;
    for (let i = 0; i < books.length; i++) {
        let data_name = books[i].name.toLowerCase();
        if (data_name.includes(name.toLowerCase())) {
            books_tag += `
            <div class="row mt-3">
                <div class="col-3">
                    <p class="mt-1">${books[i].id} : ${books[i].name} : ${books[i].price}$</p>
                </div>
                <div class="col-9">
                    <button class="btn btn-outline-dark" onclick="selectBookRent({id:'${books[i].id}', name:'${books[i].name}', price:'${books[i].price}'})" data-dismiss="modal">Select</button>
                </div>
            </div>     
        `;
        }
    }
    document.getElementById("select_books").innerHTML = books_tag.toString();
}

function selectBookRent(book) {
    let all_book = document.querySelectorAll("#book_item")

    books_item_tag = ``;
    for (let i = 0; i < all_book.length + 1; i++) {
        if (i < all_book.length) {
            books_item_tag += `
            <div class="col-12 mt-3" id="book_item" name="book_item">
                <input type="text" id="rent_book_id_${i}" name="rent_book_id_${i}" value="${document.getElementById("rent_book_id_" + i.toString()).value}" disabled> :
                <input type="text" id="rent_book_name_${i}" name="rent_book_name_${i}" value="${document.getElementById("rent_book_name_" + i.toString()).value}" disabled> :
                <input type="text" id="rent_book_price_${i}" name="rent_book_price_${i}" value="${document.getElementById("rent_book_price_" + i.toString()).value}" disabled>
            </div>
            `;
        } else {
            books_item_tag += `
            <div class="col-12 mt-3" id="book_item" name="book_item">
                <input type="text" id="rent_book_id_${i}" name="rent_book_id_${i}" value="${book.id}" disabled> :
                <input type="text" id="rent_book_name_${i}" name="rent_book_name_${i}" value="${book.name}" disabled> :
                <input type="text" id="rent_book_price_${i}" name="rent_book_price_${i}" value="${book.price}" disabled>
            </div>
            `;
        }

    }
    document.getElementById("all_book_rent").innerHTML = books_item_tag.toString();
}

function saveRent() {
    let rent_data = null;
    if (verifyDataRent()) {
        body_data = htmlBookToObject();
        var json = JSON.stringify(body_data);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/saverent");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(json);
        setTimeout(() => {
            window.location.href = '/rent';
        }, 1000);
    }
}

function verifyDataRent() {
    var verify = true;
    var error_message = null;

    if (document.querySelectorAll("#book_item").length < 1) {
        verify = false;
        error_message = 'The book must be more than 1';
    } else if (!document.getElementById("rent_member_id").value) {
        verify = false;
        error_message = 'Please select a member';
    }

    if (error_message) {
        alert(error_message);
    }
    return verify;
}

function htmlBookToObject() {
    data = {
        member: null,
        book: []
    };

    data.member = {
        id: parseInt(document.getElementById("rent_member_id").value),
        code: document.getElementById("rent_member_code").value
    }

    let all_book = document.querySelectorAll("#book_item")

    books_item_tag = ``;
    for (let i = 0; i < all_book.length; i++) {
        data.book.push({
            id: parseInt(document.getElementById("rent_book_id_" + i.toString()).value),
            name: document.getElementById("rent_book_name_" + i.toString()).value,
            price: parseInt(document.getElementById("rent_book_price_" + i.toString()).value)
        })
    }
    return data;
}

function getViewBook(data) {
    let books = data.split(",")
    books_tag = ``;
    for (let i = 0; i < books.length; i++) {
        if (books[i]) {
            books_tag += `
            <h5> ${i+1} : ${books[i]} </h5>
        `;
        }
    }
    document.getElementById("rent_view_books").innerHTML = books_tag.toString();
}