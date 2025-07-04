document.addEventListener("DOMContentLoaded", () => {
  // Save journal entry
  const saveBtn = document.getElementById("saveButton");
  if (saveBtn) {
    saveBtn.addEventListener("click", saveJournalEntry);
  }

  // Load history
  //const historyBtn = document.querySelector(".option.history");
  //if (historyBtn) {
  //  historyBtn.addEventListener("click", () => {
  //    window.location.href = "history.html";
  //  });
  //}

  // Load history list
  loadHistory();
});

function saveJournalEntry() {
  const journalText = document.getElementById("journalInput").value.trim();
  if (journalText) {
    fetch('/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: journalText }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === "success") {
        alert("Journal entry saved!");
        document.getElementById("journalInput").value = "";
        loadHistory();
      }
    })
    .catch(error => console.error('Error:', error));
  } else {
    alert("Please write something before saving.");
  }
}

function loadHistory() {
  const historyList = document.getElementById("historyList");
  if (historyList) {
    fetch('/journalList', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
      historyList.innerHTML = "";
      data.forEach(entry => {
        const li = document.createElement("li");
        li.textContent = `${entry.date}: ${entry.content.substring(0, 30)}...`;
        li.onclick = () => showDetailedEntry(entry);
        historyList.appendChild(li);
      });
    })
    .catch(error => console.error('Error:', error));
  }
}

function showDetailedEntry(entry) {
  const detailedHistory = document.getElementById("detailedHistory");
  if (detailedHistory) {
    detailedHistory.innerHTML = `<div class="history-item">Date: ${entry.date}<br>Entry: ${entry.content}</div>`;
    window.location.href = "detailed_history.html";
  }
}

document.addEventListener("DOMContentLoaded", () => {

  const saveBtn = document.getElementById("saveButton");
  if (saveBtn) {
    saveBtn.addEventListener("click", saveJournalEntry);
  }

  // Load history
  //const historyBtn = document.querySelector(".option.history");
  //if (historyBtn) {
  //  historyBtn.addEventListener("click", () => {
  //    window.location.href = "history.html";
  //  });
  //}

  // Load history list
  function clearTextbox(){
    try {
      document.getElementById("journalInput").value = "";
      
    } catch (error) {
      console.log("That was a mistake")
      
    }
  }


  loadHistory();
  clearTextbox();
});