document.addEventListener('DOMContentLoaded', function () {
    var colors = ['LightPink', 'LightGreen', 'LightBlue']
    document.querySelectorAll('.post').forEach(post => {
        post.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)]
    })

    document.querySelectorAll('.edit').forEach(btn => {
        btn.onclick = function () {
            var post_id = btn.dataset.post_id
            document.querySelector('#post_'+post_id).innerHTML = `
                <form action="" method="post">
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
        }

    })

});
