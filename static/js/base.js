function reloadWindow() {
    new Promise(
        (res, rej) => {
            setTimeout(() => res("donw"), 100);
        }
    ).then(
        (res) => {
            window.location.replace(window.location.href);
        }
    )
}


function showProjectMenu(e) {
    let target = e.target;
    let Y = target.getBoundingClientRect().y;
    let id = e.target.dataset.projectId;

    let proj_op = document.querySelector(".project-options");
    proj_op.dataset.projectId = id;
    proj_op.style.display = proj_op.style.display == "flex" ? "none" : "flex";
    proj_op.style.left = "250px";
    proj_op.style.top = Y + "px";

    proj_op.dataset.optionsFor = target.id;
    let settings_btn = proj_op.children[2];

    if (target.dataset.isSuper == 1) {
        settings_btn.style.display = "block";
    } else {
        settings_btn.style.display = "none";
    }
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
    window.location.href = "/login";
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


function handleProjectOptions(e) {
    let pID = e.target.parentElement.dataset.projectId;
    if (e.target.innerText == "Settings") {
        window.location.assign(`/project-settings/${pID}`);
    }
    if (e.target.innerText == "Tasks") {
        window.location.assign(`/tasks/${pID}`);
    }

}


function handleNotiBtn(e) {
    let notiarea = document.querySelector(".notifications");
    notiarea.style.display = notiarea.style.display == "block" ? "none" : "block";
}

function handleAcceptInvite(e) {
    fetch(`/acceptInvite?noti_id=${e.target.dataset.notiId}`, {
        credentials: 'same-origin',
    }).then((res) => {
        reloadWindow();
    })

}

function handleRejectInvite(e) {
    fetch(`/rejectInvite?noti_id=${e.target.dataset.notiId}`, {
        credentials: 'same-origin',
    }).then((res) => {
        reloadWindow();
    })
}