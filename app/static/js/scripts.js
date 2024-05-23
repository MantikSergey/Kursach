var levels = { info: "#0d6efd", error: "#dc3545", warning: "#ffc107" };


function create_toast(title, message, level = "info", time = "just now") {
    var toast_holder = document.getElementById("toast_holder")
    var toast = document.createElement("div")
    toast.classList.add("toast", "fade")
    toast.innerHTML = create_html_toast(title, message, time, levels[level])
    var toast_instance = new bootstrap.Toast(toast)
    toast_holder.appendChild(toast)
    toast_instance.show()
};
function create_html_toast(title, message, time, level) {
    return `
            <div class="toast-header">
                <svg width="25" height="25">
                    <rect fill=${level} y="3" width="20" height="20" rx="3" />
                </svg>
                <strong class="me-auto">${title}</strong>
                <small class="text-muted">${time}</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>`
};

function create_table(headers, rows) {
    let table = `
        <table class="table table-striped" id = "myTable">
        <thead>
            <tr>
            `
    headers.forEach(element => {
        table += `<td>${element}</td>`
    })

    table += `</tr>
    </thead>
    <tbody>
    `
    for(i = 0; i < rows.length; i++){
        table = table +
        `<tr>
          <th scope="row">${i}</th>
        `
        row = rows[i]
        row.forEach(element => {
            table += `<td>${element}</td>\n`
        });
        table += `</tr>\n`
    }

    table = table +
    `</tbody>
    </table>`
    return table
}

CURRENT_TRAIN = null

function reserve_button(ind) {
    html = `<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal" onclick="click_reserve(${ind})">
    Забронировать
  </button>`
    return html
}

function click_reserve(ind) {
    CURRENT_TRAIN = ind
    
    list = document.getElementById('train_time_list')
    row = TABLE_DATA.rows[ind]
    times = row[1]

    html = ''
    times.forEach(time => {
        html +=  `<li><a class="dropdown-item" onclick="change_time('${time}')">${time}</a></li>\n`
    })
    list.innerHTML = html
}

function change_time(time) {
    title = document.getElementById('train_time_title')
    title.innerText = time
}


async function reserve_button_callback(train_id) {
    date = document.getElementById('train_date').value
    time = document.getElementById('train_time_title').text
    resp = await fetch(`/api/create_train?train_id=${train_id}&date=${date}&time=${time}`, {method: 'post'})
    if (resp.ok) {
        create_toast('Информация', 'Вы забронировали занятие')
    }
    else {
        create_toast('Ошибка', 'Вы не смогли забронировать занятие', 'error')
    }
}

function delete_button(ind) {
    html = `<button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#exampleModal" onclick="delete_train(${ind})">
    Удалить запись
  </button>`
    return html
}


async function delete_train(train_id) {
    resp = await fetch(`/api/delete_train?train_id=${train_id}`, {method: 'delete'})
    if (resp.ok) {
        location.reload()
        create_toast('Информация', 'Занятие удалено')
    }
    else {
        create_toast('Ошибка', 'Произошла ошибка, невозможно удалить запись', 'error')
    }
}