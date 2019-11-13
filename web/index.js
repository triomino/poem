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

function get_books() {
    set_loading()
    const sec = document.getElementById('section').value
    httpGet('/confessio?section=' + sec, display)
}

function set_loading() {

}

function display_entries(data, eid) {
    const root = document.getElementById('entry')
    nodes = {}
    let cur = null
    JSON.parse(data).forEach(([id, ppt, forms, etymology, definition]) => {
        if (!nodes[id]) {
            cur = document.createElement('div')
            cur.classList.add('entry')
            nodes[id] = cur
            if (id == eid) {
                marker = document.createElement('div')
                marker.innerText = 'This one is chosen.'
                cur.appendChild(marker)
            }
            ppt_dom = document.createElement('div')
            ppt_dom.innerText = ppt
            f_dom = document.createElement('div')
            f_dom.innerHTML = forms
            em_dom = document.createElement('div')
            em_dom.innerHTML = etymology
            cur.appendChild(ppt_dom)
            cur.appendChild(f_dom)
            cur.appendChild(em_dom)
        } else {
            cur = nodes[id]
        }
        def_dom = document.createElement('div')
        def_dom.innerHTML = definition
        cur.appendChild(def_dom)
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

function create_word(word, tot, e_id, wid) {
    const res = document.createElement('span')
    res.innerText = word
    if (tot > 1) {
        res.classList.add('multiple_entry')
    } else if (tot === 0 || !e_id) {
        res.classList.add('no_entry')
    }
    res.onclick = () => get_entries(word, wid, e_id)
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
        cur.appendChild(create_word(word, e_cnt, e_sel, wid))
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
