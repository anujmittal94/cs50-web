document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = () => {
    send_email();
    return false;
  }

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email() {
    recipients = document.querySelector('#compose-recipients').value;
    subject = document.querySelector("#compose-subject").value;
    body = document.querySelector("#compose-body").value;
    console.log(recipients)
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
        })
    })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
      //load mailbox
      load_mailbox('sent');
    });
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  document.querySelector('#emails-view').innerHTML += `
  <div class="row border">
    <div class="col"> <b>Sender</b> </div>
    <div class="col"> <b>Subject</b> </div>
    <div class="col"> <b>Time</b> </div>
  </div>
  `
  // Access the chosen mailbox contents
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      // ... do something else with emails ...
      emails.forEach(email => {
        display(mailbox, email);
      });
  });
}

function display(mailbox, email) {
  const displaybox = document.createElement('div');
  displaybox.className += " row border";
  if (email.read) {
    displaybox.className += " read";
  }
  displaybox.innerHTML += `
    <div class = "col">${email.sender}</div>
    <div class = "col">${email.subject}</div>
    <div class = "col">${email.timestamp}</div>
  `;
  document.querySelector('#emails-view').append(displaybox);
  displaybox.addEventListener("click", () => details(mailbox, email));
}


function details(mailbox, email) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  document.querySelector('#email-view').innerHTML = `<h3>${email.subject}</h3>`;
  const detailsbox = document.createElement('div');
  detailsbox.className += " border";
  detailsbox.innerHTML += `
    <b>Sender: </b>${email.sender}<br>
    <b>Time: </b>${email.timestamp}<br>
    <b>Recipients: </b>${email.recipients}<br><br>
    <pre>${email.body}</pre>
  `
  document.querySelector('#email-view').append(detailsbox);

  if (mailbox != 'sent') {
    const archivebutton = document.createElement('button');
    archivebutton.className += " btn btn-primary";
    if (email.archived) {archivebutton.innerHTML = "Unarchive"} else {archivebutton.innerHTML = "Archive"}
    document.querySelector('#email-view').append(archivebutton);
    archivebutton.addEventListener('click', () => archive(email))
    document.querySelector('#email-view').append(" ");
    const replybutton = document.createElement('button');
    replybutton.className += " btn btn-primary";
    replybutton.innerHTML = "Reply"
    document.querySelector('#email-view').append(replybutton);
    replybutton.addEventListener('click', () => reply(email));
  }
}

function archive(email) {
  fetch(`/emails/${email.id}`, {
  method: 'PUT',
  body: JSON.stringify({
      archived: !email.archived
    })
  })
  .then(result => {
    // Print result
    console.log(result);
    //load mailbox
    load_mailbox('inbox');
  });
}

function reply(email) {
  compose_email();
  document.querySelector('#compose-recipients').value = email.sender;
  if (email.subject.startsWith("Re: ")) {
    document.querySelector('#compose-subject').value = email.subject;
  } else {
    document.querySelector('#compose-subject').value = "Re: ".concat(email.subject);
  }

  document.querySelector('#compose-body').value += `

  On ${email.timestamp}, ${email.sender} wrote:

  `
  document.querySelector('#compose-body').value += email.body;
}
