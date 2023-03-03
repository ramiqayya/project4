document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname === "/") {
        document.getElementById("edit-view").style.display = "none";
        document.getElementById("posts-view").style.display = "block";
        const likeForms = document.querySelectorAll(".like-f");

        likeForms.forEach(likeForm => {

            likeForm.addEventListener("submit", function (event) {
                event.preventDefault();
            })

            likeForm.onsubmit = function () {
                fetch('/', {
                    method: 'POST',
                    body: JSON.stringify({
                        liked_id: likeForm.dataset.tid,

                    })
                }).then(response => response.json())
                    .then(result => {
                        // Print result

                        console.log(result.likes_count)
                        document.getElementById(likeForm.dataset.tid).innerHTML = result.likes_count
                        const thisbutton = document.querySelector(`.num${likeForm.dataset.tid}`)
                        if (thisbutton.value == "Like") {
                            thisbutton.value = "Unlike"
                            thisbutton.classList.remove("btn-outline-primary")
                            thisbutton.classList.add("btn-primary")
                        } else {

                            thisbutton.value = "Like"
                            thisbutton.classList.remove("btn-primary")
                            thisbutton.classList.add("btn-outline-primary")
                        }
                    });

            }
        });

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

    }


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
                const editedTweet = document.querySelector(`.tweet${edited_p.dataset.postId}`)
                editedTweet.innerHTML = result.edit
            });
        document.getElementById("edit-view").style.display = "none";
        document.getElementById("posts-view").style.display = "block";

    }





}