//const { response } = require("express");

document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:5000/getAll')
    .then(response => response.json())
    .then(data => loadHTMLTable(data['data']));
    //.then(data => console.log(data));
    //loadHTMLTable([]);
});

const addBtn = document.getElementById("add-name-btn");
addBtn.onclick = function () {
    console.log("button pressed");
    const nameInput = document.getElementById("name-input");
    const name = nameInput.value;
    document.getElementById("name-input").value = "";
    //nameInput.innerHTML = "";

    fetch('http://localhost:5000/insert', {
        headers: {
            'Content-type': 'application/json'          
        },
        method: 'POST',
        body: JSON.stringify({name : name})
    })
    .then(response => response.json())
    .then(data => insertRowIntoTable(data['data']));
}

function insertRowIntoTable(data) {
    const table = document.querySelector('table tbody');
    const isTableData = table.querySelector('.no-data');
    let tableHtml = "<tr>";

    for (var key in data) {
        if(data.hasOwnProperty(key)) {
            if (key === 'name'){
                data[key] = data[key];
            }
            tableHtml += `<td>${data[key]}</td>`;
        }

    }

    tableHtml += `<td><button class="delete-row-btn" data-id=${data.id}>Delete</button></td>`;
    tableHtml += `<td><button class="edit-row-btn" data-id=${data.id}>Edit</button></td>`;

    if (isTableData) {
        table.innerHTML = tableHtml;
    }
    else {
        const newRow = table.insertRow();
        newRow.innerHTML = tableHtml;
    }

}

function loadHTMLTable(data) {
    const table = document.querySelector('table tbody');

    if(data.length === 0){
        table.innerHTML = "<tr><td class='no-data' colspan='4'>No Data</td></tr>";
        return;
    }
    let tableHtml = "";
    data.forEach(function ({id, name}){
        tableHtml += "<tr>";
        tableHtml += `<td>${id}</td>`;
        tableHtml += `<td>${name}</td>`;
        tableHtml += `<td><button class="delete-row-btn" data-id=${id}>Delete</button></td>`;
        tableHtml += `<td><button class="edit-row-btn" data-id=${id}>Edit</button></td>`;
        tableHtml += "</tr>";
    });
    table.innerHTML = tableHtml;
}

const searchBtn = document.querySelector('#search-btn');

searchBtn.onclick = function() {
    const searchValue = document.getElementById("search-input").value;
    fetch('http://localhost:5000/search/' + searchValue)
    .then(response => response.json())
    .then(data => loadHTMLTable(data['data']));


    document.getElementById("search-input").value = "";
}