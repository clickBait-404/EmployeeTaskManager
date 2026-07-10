/* =========================================================
   Task Management System - script.js
   Handles: form validation, edit modal (AJAX pre-fill),
   delete confirmation, and auto-dismissing flash messages.
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* ---------------------------------------------------
       0. Auto-dismiss flash messages after a few seconds
       --------------------------------------------------- */
    var flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach(function (msg) {
        setTimeout(function () {
            msg.style.transition = "opacity 0.5s ease";
            msg.style.opacity = "0";
            setTimeout(function () { msg.remove(); }, 500);
        }, 4000);
    });

    /* ---------------------------------------------------
       1. Login form validation
       --------------------------------------------------- */
    var loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            var username = document.getElementById("username");
            var password = document.getElementById("password");
            var usernameError = document.getElementById("usernameError");
            var passwordError = document.getElementById("passwordError");
            var valid = true;

            if (!username.value.trim()) {
                usernameError.style.display = "block";
                valid = false;
            } else {
                usernameError.style.display = "none";
            }

            if (!password.value.trim()) {
                passwordError.style.display = "block";
                valid = false;
            } else {
                passwordError.style.display = "none";
            }

            if (!valid) {
                e.preventDefault();
            }
        });
    }

    /* ---------------------------------------------------
       2. Add Task form validation (Admin dashboard)
       --------------------------------------------------- */
    var taskForm = document.getElementById("taskForm");
    if (taskForm) {
        taskForm.addEventListener("submit", function (e) {
            if (!validateTaskFields("employee_id", "task_title", "completed",
                                     "employeeError", "taskTitleError", "completedError")) {
                e.preventDefault();
            }
        });
    }

    /* ---------------------------------------------------
       3. Generic field validator used by both add & edit forms
       --------------------------------------------------- */
    function validateTaskFields(empFieldId, titleFieldId, completedFieldId,
                                 empErrId, titleErrId, completedErrId) {
        var emp = document.getElementById(empFieldId);
        var title = document.getElementById(titleFieldId);
        var completed = document.getElementById(completedFieldId);
        var empErr = document.getElementById(empErrId);
        var titleErr = document.getElementById(titleErrId);
        var completedErr = document.getElementById(completedErrId);
        var valid = true;

        if (!emp.value) {
            empErr.style.display = "block";
            valid = false;
        } else {
            empErr.style.display = "none";
        }

        if (!title.value) {
            titleErr.style.display = "block";
            valid = false;
        } else {
            titleErr.style.display = "none";
        }

        if (!completed.value) {
            completedErr.style.display = "block";
            valid = false;
        } else {
            completedErr.style.display = "none";
        }

        return valid;
    }

    /* ---------------------------------------------------
       4. Delete confirmation
       --------------------------------------------------- */
    var deleteForms = document.querySelectorAll(".delete-form");
    deleteForms.forEach(function (form) {
        form.addEventListener("submit", function (e) {
            var confirmed = window.confirm("Are you sure you want to delete this task?");
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

    /* ---------------------------------------------------
       5. Edit Task modal (Admin dashboard)
       --------------------------------------------------- */
    var editModal = document.getElementById("editModal");
    var editForm = document.getElementById("editTaskForm");
    var editButtons = document.querySelectorAll(".btn-edit");
    var cancelEditBtn = document.getElementById("cancelEditBtn");

    if (editModal && editForm) {
        editButtons.forEach(function (btn) {
            btn.addEventListener("click", function () {
                var taskId = btn.getAttribute("data-task-id");
                var fetchUrl = window.EDIT_TASK_URL_BASE + taskId;

                fetch(fetchUrl, {
                    method: "GET",
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                })
                    .then(function (res) {
                        if (!res.ok) { throw new Error("Failed to load task."); }
                        return res.json();
                    })
                    .then(function (task) {
                        document.getElementById("editTaskIdDisplay").textContent = "Task #" + task.task_id;
                        document.getElementById("edit_employee_id").value = task.employee_id;
                        document.getElementById("edit_task_title").value = task.task_title;
                        document.getElementById("edit_completed").value = task.completed ? "True" : "False";

                        editForm.setAttribute("action", fetchUrl);
                        editModal.classList.add("open");
                    })
                    .catch(function () {
                        alert("Could not load task details. Please try again.");
                    });
            });
        });

        if (cancelEditBtn) {
            cancelEditBtn.addEventListener("click", function () {
                editModal.classList.remove("open");
            });
        }

        // Close modal when clicking outside the box
        editModal.addEventListener("click", function (e) {
            if (e.target === editModal) {
                editModal.classList.remove("open");
            }
        });

        editForm.addEventListener("submit", function (e) {
            if (!validateTaskFields("edit_employee_id", "edit_task_title", "edit_completed",
                                     "editEmployeeError", "editTaskTitleError", "editCompletedError")) {
                e.preventDefault();
            }
        });
    }

});
