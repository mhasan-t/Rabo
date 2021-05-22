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