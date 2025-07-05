console.log("chekcing the name of the website")
const path = window.location.pathname;
console.log(path);



function checkbutton(){
  if (path == "/journal"){
    document.addEventListener("DOMContentLoaded", () => {
  // Save journal entry
    const saveBtn = document.getElementById("saveButton");
    if (saveBtn) {
      saveBtn.addEventListener("click", saveJournalEntry);
    }
    loadHistory();
  });
  }}


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
        console.log(data.journal_id)
        window.location.href = `/result/${data.journal_id}`;
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

function clearTextbox(){
    try {
      if (path == "/journal"){
        console.log("inside cleartextbox");
        document.getElementById("journalInput").value = "";

      }
      
      
    } catch (error) {
      console.log("That was a mistake")
      
    }
  }

  function populateRearPage(){
    console.log("inside populateRearPage");
    if (path == "/history") {
      console.log("inside detailed result")
    fetch('//journalList', {
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
  }

  }

function populateDetailedResult(){

    if (path == "/detailed_history") {
      console.log("inside detailed result")
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

function copyTextareaToHidden() {
      const journalText = document.getElementById("journalInput").value;
      document.getElementById("hiddenTextInput").value = journalText;
    }


/* ----------  RUN ON EVERY PAGE LOAD ---------- */
document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;

  if (path === "/history") {
    loadHistory();         // fills left‑hand “History” list
    loadSummaryPanels();   // fills Emotional Range / Trail Marks / Risk Levels
  }
});

/* ----------  LOAD ALL JOURNALS (LEFT PANEL) ---------- */
function loadHistory() {
  fetch("/journalList", { method: "POST" })
    .then(r => {
      if (!r.ok) throw new Error("Failed to fetch journal list");
      return r.json();
    })
    .then(entries => {
      const ul = document.getElementById("historyList") || createHistoryList();
      ul.innerHTML = "";

      entries.forEach(entry => {
        // You control which fields come from get_journal_list()
        // Here: entry.id, entry.journal_input, entry.created_time
        const li = document.createElement("li");
        li.textContent = `${formatDate(entry.created_time)} — ${truncate(entry.journal_input, 35)}`;
        li.dataset.id = entry.id;

        // When you click a single entry, fetch its details & update right panel
        li.addEventListener("click", () => loadJournalDetail(entry.id));
        ul.appendChild(li);
      });
    })
    .catch(err => console.error(err));
}

/* ----------  LOAD ONE JOURNAL DETAIL (RIGHT PANEL) ---------- */
function loadJournalDetail(journalId) {
  fetch(`/journalDetail/${journalId}`)
    .then(r => {
      if (!r.ok) throw new Error("Failed to fetch journal detail");
      return r.json();
    })
    .then(detail => {
      populateUl("emotionalRange", detail.emotions || []);
      populateUl("trailMarks",     detail.themes   || []);
      populateUl("riskLevels",     buildRiskText(detail.scores || []));
    })
    .catch(err => console.error(err));
}

/* ----------  LOAD SUMMARY FOR RIGHT PANEL ON FIRST VISIT ---------- */
function loadSummaryPanels() {
  // You can call summary endpoints here if you like, but for now just clear lists
  populateUl("emotionalRange", []);
  populateUl("trailMarks",     []);
  populateUl("riskLevels",     []);
}

/* ----------  UTIL HELPERS ---------- */
function populateUl(id, items) {
  const ul = document.getElementById(id);
  ul.innerHTML = "";
  if (items.length === 0) {
    ul.innerHTML = "<li>—</li>";
    return;
  }
  items.forEach(t => {
    const li = document.createElement("li");
    li.textContent = t;
    ul.appendChild(li);
  });
}

function createHistoryList() {
  const section = document.querySelector(".section.history");
  const ul = document.createElement("ul");
  ul.id = "historyList";
  section.appendChild(ul);
  return ul;
}
function truncate(str, n) {
  return str.length > n ? str.slice(0, n) + "…" : str;
}
function formatDate(iso) {
  return new Date(iso).toLocaleDateString();
}
function buildRiskText(scores) {
  // Convert scores list → array of "PHQ9 9 (mild)" style strings
  return scores.map(s => `${s.score_type.toUpperCase()} ${s.total_score} (${s.severity})`);
}

  
  loadHistory();
  clearTextbox();
  //checkbutton();
  populateRearPage();
  

;