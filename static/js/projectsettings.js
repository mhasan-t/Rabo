function updateProj(e) {
    let errMsg = document.querySelector("#error-msg");

    const csrftoken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];


    let fd = new FormData();
    fd.append('field', e.target.previousElementSibling.name);
    fd.append('data', e.target.previousElementSibling.value);

    let xhttp = new XMLHttpRequest();
    xhttp.open('POST', `/project-settings/${e.target.dataset.id}`, true);
    xhttp.setRequestHeader('X-CSRFToken', csrftoken);
    xhttp.send(fd);

    xhttp.onreadystatechange = () => {
        if (xhttp.status == 200) {
            errMsg.style.display = "block";
            errMsg.style.color = "green";
            errMsg.style.borderColor = "green";
            errMsg.innerHTML = "Success";
        } else {
            errMsg.style.display = "block";
            errMsg.style.color = "red";
            errMsg.style.borderColor = "red";
            errMsg.innerHTML = "An Error Occured";
        }
    }
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
                row.classList.add("flex-space-between");

                let fn = document.createTextNode(res[i].first_name)
                let ln = document.createTextNode(" " + res[i].last_name)
                let name = document.createElement("div");
                name.appendChild(fn);
                name.appendChild(ln);
                // td1.style.display = "block";
                // td2.style.display = "block";
                // td2.style.marginLeft = "5px";
                row.appendChild(name);

                let inviteBtn = document.createElement("button");
                inviteBtn.classList.add("inviteBtn");
                inviteBtn.innerText = "Invite";
                inviteBtn, addEventListener("click", () => {
                    let pid = document.querySelector("#pid").innerText;
                    let uid = res[i].id;
                    handleInviteUser(pid, uid);
                });
                row.appendChild(inviteBtn);

                resArea.appendChild(row);
            }
        }
    )

}

function handleInviteUser(pid, uid) {
    console.log(uid + " invited to " + pid);
}

function handleProjectUsers(e) {
    let pid = document.querySelector("#pid").innerText;
    let uid = e.target.dataset.uid;
    let action = e.target.dataset.action;

    let yes = confirm("Are you sure?");
    if (yes == null) {
        return;
    }

    fetch(`/project-actions/${pid}?action=${action}&on_user=${uid}`), {
            credentials: 'same-origin',
        }
        .then((res) => {
            if (res.status == 200) {
                window.location.assign(window.location.href);
            } else {
                alert("Something went wrong!");
            }
        });

}