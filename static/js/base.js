function showProjectMenu(e) {
    let target = e.target;
    let Y = target.getBoundingClientRect().y;

    let proj_op = document.querySelector(".project-options");
    proj_op.style.display = proj_op.style.display == "flex" ? "none" : "flex";
    proj_op.style.left = "250px";
    proj_op.style.top = Y + "px";

    proj_op.dataset.optionsFor = target.id;
}

function handleUserBtn(e) {
    let editUserForm = document.querySelector(".edit-user-info");
    editUserForm.style.display = editUserForm.style.display == "block" ? "none" : "block";
}

function handleUserInfoEdit(e) {
    let ipArea = e.target.previousElementSibling;
    let saveBtn = e.target.nextElementSibling
    e.target.style.display = "none";
    saveBtn.style.display = "block";
    ipArea.disabled = false;
}

function handleUserInfoSave(e) {
    let errMsg = document.querySelector("#editUserErrMsg");
    if (e.target.previousElementSibling.name == "password") {
        let field = "password";
        let newData = e.target.previousElementSibling.value;
        console.log(newData);
        if (newData == "") {
            errMsg.style.color = "red";
            errMsg.innerHTML = "Empty Password!";
            return;
        }

        e.target.parentElement.style.display = "none";
        document.querySelector("#cngPassBtn").style.display = "block";

        const csrftoken = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            .split('=')[1];

        let fd = new FormData();
        fd.append('field', field);
        fd.append('data', newData);

        let xhttp = new XMLHttpRequest();
        xhttp.open('POST', '/edit-user', true);
        xhttp.setRequestHeader('X-CSRFToken', csrftoken);
        xhttp.send(fd);


        xhttp.onreadystatechange = () => {
            if (xhttp.status == 200) {
                errMsg.style.color = "green";
                errMsg.innerHTML = "Success";
            } else {
                errMsg.style.color = "red";
                errMsg.innerHTML = "An Error Occured";
            }
        }

        return;
    }



    let ipArea = e.target.previousElementSibling.previousElementSibling;
    let field = ipArea.name;
    let newData = ipArea.value;
    ipArea.disabled = true;
    let editbtn = e.target.previousElementSibling;

    if (newData == "") {
        errMsg.style.color = "red";
        errMsg.innerHTML = "Empty Value!";
        return;
    }

    e.target.style.display = "none";
    editbtn.style.display = "block";

    const csrftoken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];

    let fd = new FormData();
    fd.append('field', field);
    fd.append('data', newData);

    let xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/edit-user', true);
    xhttp.setRequestHeader('X-CSRFToken', csrftoken);
    xhttp.send(fd);

    xhttp.onreadystatechange = () => {
        if (xhttp.status == 200) {
            errMsg.style.color = "green";
            errMsg.innerHTML = "Success";
        } else {
            errMsg.style.color = "red";
            errMsg.innerHTML = "An Error Occured";
        }
    }

    // fetch('/edit-user', {
    //     method: 'POST',
    //     headers: {
    //         'Accept': 'application/json',
    //         'Content-Type': 'application/json',
    //         'X-CSRFToken': csrftoken,
    //     },
    //     credentials: 'same-origin',
    //     body: JSON.stringify({
    //         field: field,
    //         data: newData,
    //     }),
    // }).then(
    //     (res) => {
    //         let errMsg = document.querySelector("#editUserErrMsg");
    //         if (res.status != 200) {
    // errMsg.style.color = "red";
    // errMsg.innerHTML = "An Error Occured";
    //         } else {
    // errMsg.style.color = "green";
    // errMsg.innerHTML = "Success";
    //         }
    //     }
    // );
}

function handlePictureUpload(e) {
    const csrftoken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];

    let pic = document.querySelector("#id_picture").files[0];
    let errMsg = document.querySelector("#editUserErrMsg");

    if (pic == undefined) {
        errMsg.style.color = "red";
        errMsg.innerHTML = "Please select an image.";
        return;
    }

    let fd = new FormData();
    fd.append('field', 'picture');
    fd.append('pic', pic);

    let xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/edit-user', true);
    xhttp.setRequestHeader('X-CSRFToken', csrftoken);
    xhttp.send(fd);

    xhttp.onreadystatechange = () => {
        if (xhttp.status == 200) {
            errMsg.style.color = "green";
            errMsg.innerHTML = "Success";
            window.location.href = window.location.href;
        } else {
            errMsg.style.color = "red";
            errMsg.innerHTML = "An Error Occured";
        }
    }



    // fetch('/edit-user', {
    //     method: 'POST',
    //     headers: {
    //         'Accept': 'application/json',
    //         'Content-Type': 'application/json',
    //         'X-CSRFToken': csrftoken,
    //     },
    //     credentials: 'same-origin',
    //     body: fd
    // }).then(
    //     (res) => {
    // if (res.status != 200) {
    //     errMsg.style.color = "red";
    //     errMsg.innerHTML = "An Error Occured";
    // } else {
    //     errMsg.style.color = "green";
    //     errMsg.innerHTML = "Success";
    // }
    //     }
    // );

}

function handleChangePass(e) {
    document.querySelector("#cngPass").style.display = "block";
    e.target.style.display = "none";
}

function handleLogout(e) {
    document.cookie = "session_id= ; expires = Thu, 01 Jan 1970 00:00:00 GMT";
    window.location.assign("login");
}

function handleDeleteUser(e) {
    let confirmDel = confirm("Are you sure you want to delete your account?");
    if (!confirmDel) {
        return;
    }

    const csrftoken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
    let errMsg = document.querySelector("#editUserErrMsg");

    fetch('/delete-user', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        credentials: 'same-origin',
    }).then(
        (res) => {
            if (res.status != 200) {
                errMsg.style.color = "red";
                errMsg.innerHTML = "An Error Occured";
            } else {
                window.location.assign("signup");
            }
        }
    )
}

function handleSearchUser(e) {
    let resArea = document.querySelector("#searchRes");

    function cleanResArea() {
        resArea.innerHTML = "";
    }

    const csrftoken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];

    if (e.target.value == "") {
        resArea.style.display = "none";
        return;
    } else {
        resArea.style.display = "flex";
    }



    fetch(
        "/search-user?query=" + e.target.value
    ).then(
        (res) => {
            if (res.status == 200) {
                return res.json();
            }
            return false;
        }
    ).then(
        (res) => {
            if (!res) {
                return;
            }
            cleanResArea();
            for (let i = 0; i < res.length; i++) {
                let row = document.createElement("div");
                let fn = document.createTextNode(res[i].first_name)
                let ln = document.createTextNode(" " + res[i].last_name)

                let td1 = document.createElement("span");
                let td2 = document.createElement("span");
                td1.appendChild(fn);
                td2.appendChild(ln);
                // td1.style.display = "block";
                // td2.style.display = "block";
                // td2.style.marginLeft = "5px";

                row.appendChild(td1);
                row.appendChild(td2);

                resArea.appendChild(row);
            }
        }
    )

}