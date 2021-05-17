document.addEventListener('DOMContentLoaded', function () {
    var colors = ['LightPink', 'LightGreen', 'LightBlue']
    document.querySelectorAll('.post').forEach(post => {
        post.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)]
    })
})
