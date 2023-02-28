document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("edit-view").style.display = "none";
    document.getElementById("posts-view").style.display = "block";

    const editButtons = document.querySelectorAll(".edit-b");
    editButtons.forEach(button => {
        button.onclick = function () {
            fetch(`edit/${button.dataset.pid}`)
                .then(response => response.json())
                .then(posts => {
                    document.querySelector("#edit-text").innerHTML = posts.tweet,
                        document.querySelector("#edit-text").dataset.postId = posts.id
                    console.log(posts.tweet)
                    console.log(posts.id)
                })
        }

        button.addEventListener("click", edit_post)

    });




})

function edit_post() {

    document.getElementById("edit-view").style.display = "block";
    document.getElementById("posts-view").style.display = "none";
    const saveForm = document.getElementById("edit-form")

    saveForm.addEventListener("submit", function (event) {
        event.preventDefault();
    })

    saveForm.onsubmit = function () {
        const edited_p = document.querySelector("#edit-text")
        fetch('/save_changes', {
            method: 'POST',

            body: JSON.stringify({
                edited_post: edited_p.value,
                post_id: edited_p.dataset.postId


            })
        }).then(response => response.json())
            .then(result => {
                // Print result
                console.log(result);
            });
        document.getElementById("edit-view").style.display = "none";
        document.getElementById("posts-view").style.display = "block";

    }





}