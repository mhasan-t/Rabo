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



document.querySelector("#id_category").addEventListener("focusout", (event) => {
    new Promise(function (resolve, reject) {
        setTimeout(() => resolve("done"), 200);
    }).then((res) => {
        document.querySelector("#searchRes").innerHTML = "";
        document.querySelector("#searchRes").style.display = "none";
    });
})
document.querySelector("#id_assigned_to").addEventListener("focusout", (event) => {
    new Promise(function (resolve, reject) {
        setTimeout(() => resolve("done"), 200);
    }).then((res) => {
        document.querySelector("#searchUserRes").innerHTML = "";
        document.querySelector("#searchUserRes").style.display = "none";
    });

})



function handleShowCats(e) {

    let resArea = document.querySelector("#searchRes");
    let pid = e.target.dataset.pid;

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
        `/showcats/${pid}?query=${e.target.value}`
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
                row.classList.add("catValue");

                let fn = document.createTextNode(res[i]);

                row.appendChild(fn);
                resArea.appendChild(row);
            }

            document.querySelectorAll(".catValue").forEach((item, index) => {
                item.addEventListener("click", (ee) => {
                    document.querySelector("#id_category").value = ee.target.innerText;
                    cleanResArea();
                    resArea.style.display = "none";
                });
            })

        }

    )
}


function handleShowManagers(e) {
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

    let pid = e.target.dataset.pid;
    let taskid = e.target.dataset.taskid;

    fetch(
        `/showmanagers/${pid}/${taskid}?query=${e.target.value}`
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
                name.classList.add("selectManager");
                name.dataset.uid = res[i].id;
                row.appendChild(name);

                row.dataset.uid = res[i].id;
                resArea.appendChild(row);
            }

            document.querySelectorAll(".selectManager").forEach(
                (item, index) => {
                    item.addEventListener("click", () => {
                        e.target.value = item.dataset.uid;
                        cleanResArea();
                        resArea.style.display = "none";
                    });
                }
            )

        }
    )

}

function handleShowUsers(e) {

    let resArea = document.querySelector("#searchUserRes");
    let pid = e.target.dataset.pid;

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
        `/showusers/${pid}?query=${e.target.value}`
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
                row.classList.add("userValue");
                row.dataset.uid = res[i].id

                let fn = document.createTextNode(res[i].first_name)
                let ln = document.createTextNode(" " + res[i].last_name)
                let name = document.createElement("div");
                name.appendChild(fn);
                name.appendChild(ln);

                row.appendChild(name);
                resArea.appendChild(row);
            }

            document.querySelectorAll(".userValue").forEach((item, index) => {
                item.addEventListener("click", (ee) => {
                    document.querySelector("#id_assigned_to").value = item.dataset.uid;
                    cleanResArea();
                    resArea.style.display = "none";
                });
            })

        }

    )
}


function handleShowTasks(e) {
    let resArea = document.querySelector("#searchTaskRes");
    let pid = e.target.dataset.pid;
    let taskid = e.target.dataset.taskid;

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
        `/showtasks/${pid}/${taskid}?query=${e.target.value}`
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
                row.classList.add("taskValue");
                row.dataset.indTask = res[i][0]

                let label = document.createElement("div");
                label.appendChild(document.createTextNode(res[i][1]));

                let actionBtn = document.createElement("button");

                if (res[i][2] == 0) {
                    actionBtn.classList.add("addBtn");
                    actionBtn.classList.add("yesBtn");
                    actionBtn.innerText = "Add";
                } else {
                    actionBtn.classList.add("removeBtn");
                    actionBtn.classList.add("noBtn");
                    actionBtn.innerText = "Remove";
                }


                row.appendChild(label);
                row.appendChild(actionBtn);
                resArea.appendChild(row);
            }

            document.querySelectorAll(".addBtn").forEach((item, index) => {
                item.addEventListener("click", (ee) => {

                    fetch(`/addtaskDependency/${pid}/${taskid}?independent=${item.parentElement.dataset.indTask}`)

                    cleanResArea();
                    resArea.style.display = "none";
                    new Promise(
                        (res, rej) => {
                            setTimeout(() => res("donw"), 100);
                        }
                    ).then(
                        (res) => {
                            window.location.replace(window.location.href);
                        }
                    )
                });
            })

            document.querySelectorAll(".removeBtn").forEach((item, index) => {
                item.addEventListener("click", (ee) => {

                    fetch(`/removetaskDependency/${pid}/${taskid}?independent=${item.parentElement.dataset.indTask}`)

                    cleanResArea();
                    resArea.style.display = "none";
                    new Promise(
                        (res, rej) => {
                            setTimeout(() => res("donw"), 100);
                        }
                    ).then(
                        (res) => {
                            window.location.replace(window.location.href);
                        }
                    )
                });
            })

        }

    )
}



function handleSubmitTask(e) {
    let taskid = e.target.dataset.taskid;
    let pid = e.target.dataset.pid;

    let yes = confirm("Are you sure you want submit this task?");
    if (yes == false) {
        return;
    }

    fetch(`/submitTask/${pid}/${taskid}`, {
        credentials: 'same-origin',
    })
}

function handleEndTask(e) {
    let taskid = e.target.dataset.taskid;
    let pid = e.target.dataset.pid;

    let yes = confirm("Are you sure you want end this task?");
    console.log(yes);
    if (yes == false) {
        return;
    }

    fetch(`/endTask/${pid}/${taskid}`, {
        credentials: 'same-origin',
    }).then((res) => {
        reloadWindow();
    })
}


function handleSendReminder(e) {
    let taskid = e.target.dataset.taskid;
    let pid = e.target.dataset.pid;


    fetch(`/sendReminder/${pid}/${taskid}`, {
        credentials: 'same-origin',
    }).then((res) => {
        alert("Sent");
    })
}