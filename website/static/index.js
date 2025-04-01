// function deleteNote(noteId) {
//   const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content"); 
//   fetch('/delete-note', {
//     method:'POST',
//     body: JSON.stringify({noteId: noteId}),
//     headers:{
//       'Content-Type': 'application/json',
//       "X-CSRFToken": csrfToken, 
//     }
//   }).then((_res) => {
//     window.location.href = "/"; /*this is how we reload the window with the get request specifically: redirect us to the homepage refresh the page */
//   });
// }  
// /* take the noteId that we pass and gonna send a post request to the delete-note end point, after we get response from this delete-note end point 
// it's going to reload the window */