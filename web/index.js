const sec_list = {
    'P': 'Prologue',
    '1': 'Book 1',
    '2': 'Book 2',
    '3': 'Book 3',
    '4': 'Book 4',
    '5': 'Book 5',
    '6': 'Book 6',
    '7': 'Book 7',
    '8': 'Book 8'
}

function fill_options() {
    const select_sec = document.getElementById('section')
    for (key in sec_list) {
        op = document.createElement('option')
        op.value = key
        op.innerText = sec_list[key]
        select_sec.appendChild(op)
    }
}

function load_cache(key) {
    return localStorage[key]
}

const bookKey = 'selectedBook'
function init() {
    fill_options()
    last_book_value = load_cache(bookKey)
    if (last_book_value in sec_list) {
        document.getElementById('section').value = last_book_value
    }
}

function save_cache(key, value) {
    localStorage.setItem(key, value)
}

function get_books() {
    set_loading()
    const sec = document.getElementById('section').value
    if (sec in sec_list) {
        httpGet('/confessio?section=' + sec, display)
    }
    save_cache(bookKey, sec)
}

function set_loading() {

}

let nodes = {}
let def = {}

function display_entries(data, eid) {
    const root = document.getElementById('entry')
    let cur = null
    nodes = {}
    def = {}
    JSON.parse(data).forEach(([id, ppt, forms, etymology, definition, word]) => {
        if (!nodes[id]) {
            cur = document.createElement('div')
            cur.classList.add('entry')
            if (id == eid) {
                const marker = document.createElement('div')
                marker.innerText = 'This one is chosen.'
                cur.appendChild(marker)
            }
            const word_dom = document.createElement('span')
            word_dom.classList.add('HI_B')
            word_dom.innerText = word
            cur.appendChild(word_dom)
            const ppt_dom = document.createElement('span')
            ppt_dom.innerText = ppt
            cur.appendChild(ppt_dom)
            // row1
            const f_dom = document.createElement('td')
            f_dom.innerHTML = forms
            const form_head = document.createElement('td')
            form_head.innerText = 'Forms'
            const row1_dom = document.createElement('tr')
            row1_dom.appendChild(form_head)
            row1_dom.appendChild(f_dom)
            // row2
            const em_dom = document.createElement('td')
            em_dom.innerHTML = etymology
            const em_head = document.createElement('td')
            em_head.innerText = 'Etymology'
            const row2_dom = document.createElement('tr')
            row2_dom.appendChild(em_head)
            row2_dom.appendChild(em_dom)
            // table
            const table_dom = document.createElement('table')
            table_dom.appendChild(row1_dom)
            table_dom.appendChild(row2_dom)
            cur.appendChild(table_dom)
            // collapse
            const show_link = document.createElement('button')
            const hide_link = document.createElement('button')
            show_link.onclick = () => {
                nodes[id].appendChild(hide_link)
                nodes[id].appendChild(def[id])
                nodes[id].removeChild(show_link)
            }
            show_link.innerText = 'Show Definitions'
            hide_link.onclick = () => {
                nodes[id].appendChild(show_link)
                nodes[id].removeChild(def[id])
                nodes[id].removeChild(hide_link)
            }
            hide_link.innerText = 'Hide Definitions'
            cur.appendChild(show_link)
            // put <id, node>
            nodes[id] = cur
            def[id] = document.createElement('div')
            def[id].id = 'def' + id
        }
        const def_dom = document.createElement('div')
        def_dom.innerHTML = definition
        def[id].appendChild(def_dom)
    })
    Object.values(nodes).forEach((node) => {
        root.appendChild(node)
    })
}

function get_entries(word, wid, eid) {
    e = document.getElementById('entry')
    e.innerText = word
    httpGet('/entry?word=' + wid, (data) => display_entries(data, eid, e))
}

let last_chosen = null
function set_selected_word(selected) {
    if (last_chosen) {
        last_chosen.classList.toggle('big_word')
    }
    selected.classList.toggle('big_word')
    last_chosen = selected
}

function create_word(row, column, word, tot, e_id, wid) {
    const res = document.createElement('span')
    res.innerText = word
    if (tot > 1) {
        res.classList.add('multiple_entry')
    } else if (tot === 0 || !e_id) {
        res.classList.add('no_entry')
    }
    res.onclick = () => {
        set_selected_word(res)
        get_entries(word, wid, e_id) 
    }
    return res
}

function display(data) {
    const root = document.getElementById('confessio')
    let cur = {row: -1}
    JSON.parse(data).forEach(([r, c, word, e_cnt, e_sel, wid]) => {
        if (r !== cur.row) {
            if (cur.row !== -1) {
                root.appendChild(cur)
            }
            cur = document.createElement('div')
            cur.row = r
        }
        cur.appendChild(create_word(r, c, word, e_cnt, e_sel, wid))
    })
    root.appendChild(cur)
}

function httpGet(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}
