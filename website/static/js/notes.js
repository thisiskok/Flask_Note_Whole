function showAddForm() {
  const addForm = document.getElementById("noteForm");
  const editForm = document.getElementById("editForm");
  const addNoteBtn = document.getElementById("add-note-btn");

  addForm.style.display = "block";
  editForm.style.display = "none";
  addNoteBtn.style.display = "none";
}

function showEditForm(id, title, description, tag) {
  const addForm = document.getElementById("noteForm");
  const editForm = document.getElementById("editForm");
  const addNoteBtn = document.getElementById("add-note-btn");

  document.getElementById("edit-note-id").value = id;
  document.getElementById("edit-note-title").value = title;
  document.getElementById("edit-note-description").value = description;
  document.getElementById("edit-note-tag").value = tag;

  editForm.style.display = "block";
  addForm.style.display = "none";
  addNoteBtn.style.display = "none";
}

function hideForms() {
  const addForm = document.getElementById("noteForm");
  const editForm = document.getElementById("editForm");
  const addNoteBtn = document.getElementById("add-note-btn");

  addForm.style.display = "none";
  editForm.style.display = "none";
  addNoteBtn.style.display = "block";
}

function showFullText(id) {
  document.getElementById("short-" + id).style.display = "none";
  document.getElementById("full-" + id).style.display = "inline";
}

function showShortText(id) {
  document.getElementById("short-" + id).style.display = "inline";
  document.getElementById("full-" + id).style.display = "none";
}

function filterNotes(tag) {
  const normalizedTag = tag.trim().toLowerCase();
  const notes = document.getElementsByClassName("note-card");

  for (let i = 0; i < notes.length; i++) {
    const noteTag = (notes[i].getAttribute("data-tag") || "")
      .trim()
      .toLowerCase();

    if (normalizedTag === "all" || noteTag === normalizedTag) {
      notes[i].style.display = "block";
    } else {
      notes[i].style.display = "none";
    }
  }
}

function showShareForm(noteId) {
  const modal = document.getElementById("shareFormModal");
  document.getElementById("share-note-id").value = noteId;
  document.getElementById("shareForm").action = `/share-note/${noteId}`;
  modal.style.display = "block";
}

function hideShareForm() {
  const modal = document.getElementById("shareFormModal");
  modal.style.display = "none";
}

function deleteNote(noteId) {
  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  }).then((_res) => {
    window.location.href = "/";
  });
}

// Initialize event listeners when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  const filterLinks = document.querySelectorAll(".nav-link");
  filterLinks.forEach(function (link) {
    link.addEventListener("click", function () {
      const tag = this.textContent.trim().toLowerCase();
      filterNotes(tag);
      filterLinks.forEach(function (link) {
        link.classList.remove("active");
      });
      this.classList.add("active");
    });
  });
}); 