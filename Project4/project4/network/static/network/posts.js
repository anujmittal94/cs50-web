document.addEventListener('DOMContentLoaded', function () {
    let colors = ['LightPink', 'LightGreen', 'LightBlue']
    document.querySelectorAll('.post').forEach(post => {
        post.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)]
    })

    document.querySelectorAll('.edit').forEach(btn => {
        btn.onclick = function () {
            btn.style.display = "none"
            let post_id = btn.dataset.post_id
            document.querySelector('#post_text_'+post_id).innerHTML = `
                <form id="edit_post_form_${post_id}" action="">
                    <div class="form-group" style="padding: 10px 10px 10px 10px;">
                        <textarea
                         id="edit_post_text_${post_id}"
                         class="form-control textarea"
                         maxlength="500">${document.querySelector('#post_text_'+post_id).innerHTML}</textarea>
                        <span id="edit_post_count_${post_id}">500 words remaining</span>
                        <input class="btn btn-dark" type="submit" value="Post" style="float: right;">
                    </div>
                </form>
            `
            document.querySelector("#edit_post_text_"+post_id).oninput = function () {
                document.querySelector("#edit_post_count_"+post_id).innerHTML = (500 - this.value.length) + " characters remaining.";
            }

            document.querySelector("#edit_post_form_"+post_id).onsubmit = function () {
                    let edited_post_text = document.querySelector("#edit_post_text_"+post_id).value
                    fetch("/edit/"+post_id, {
                        method:'PUT',
                        body:JSON.stringify({edited_post_text})
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.error) {
                            console.log(result.error)
                        }
                        else {
                            console.log(result.message)
                            document.querySelector("#post_text_"+post_id).innerHTML = edited_post_text
                            btn.style.display = "inline"
                        }
                    })
                    return false;
            }
        }

    })

    document.querySelectorAll('.like').forEach(btn => {
        btn.onclick = function () {
            let post_id = btn.dataset.post_id
            fetch("/like/"+post_id, {
                method:'PUT'
            })
            .then(response => response.json())
            .then(result => {
                if (result.error) {
                    console.log(result.error)
                }
                else {
                    console.log(result.message)
                    console.log(result.likes_num+" Likes")
                    if (btn.innerHTML == "Like") {
                        btn.innerHTML = "Unlike"
                    }
                    else {
                        btn.innerHTML = "Like"
                    }
                    document.querySelector("#post_likes_"+post_id).innerHTML = result.likes_num + " Likes"
                }
            })
        }
    });

    document.querySelectorAll('.delete').forEach(btn => {
        btn.onclick = function () {
            let post_id = btn.dataset.post_id
            fetch("/delete/"+post_id, {
                method:'PUT'
            })
            .then(response => response.json())
            .then(result => {
                if (result.error) {
                    console.log(result.error)
                }
                else {
                    console.log(result.message)
                    document.querySelector('#post_'+post_id).style.display = "none"
                }
            })
        }
    });

});
