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
    let pid = document.querySelector("#pid").innerText;
    let resArea = document.querySelector("#searchRes");

    function cleanResArea() {
        resArea.innerHTML = "";
    }

    if (e.target.value == "") {
        resArea.style.display = "none";
        return;
    } else {
        resArea.style.display = "flex";
    }



    fetch(
        `/search-user/${pid}?query=${e.target.value}`
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

                row.appendChild(inviteBtn);
                row.dataset.uid = res[i].id;
                resArea.appendChild(row);
            }

            document.querySelectorAll(".inviteBtn").forEach(
                (item, index) => {
                    item.addEventListener("click", () => {
                        let pid = document.querySelector("#pid").innerText;
                        let uid = item.parentElement.dataset.uid;
                        handleInviteUser(pid, uid);
                    });
                }
            )

        }
    )

}

function handleInviteUser(pid, uid) {
    console.log("object");
    const csrftoken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];


    fetch(`/sendNotif/${pid}`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        credentials: 'same-origin',
        body: JSON.stringify({
            type: 'invite',
            sent_to: uid,
            data: ""
        })

    }).then((res) => {
        reloadWindow();
    })

}

function handleProjectUsers(e) {
    let pid = document.querySelector("#pid").innerText;
    let uid = e.target.dataset.uid;
    let action = e.target.dataset.action;

    let yes = confirm("Are you sure?");
    if (yes == false) {
        return;
    }

    fetch(`/project-actions/${pid}?action=${action}&on_user=${uid}`, {
            credentials: 'same-origin',
        })
        .then((res) => {
            if (res.status == 200) {
                reloadWindow();
            } else {
                alert("Something went wrong!");
            }
        });

}