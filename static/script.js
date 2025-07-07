/*document.addEventListener("DOMContentLoaded", () => {
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
});*/

/*function saveJournalEntry() {
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
        console.log(data)
        document.getElementById("journalInput").value = "";
        window.location.href = `/result?id=${data.journal_id}`;
        loadHistory();
      }
    })
    .catch(error => console.error('Error:', error));
  } else {
    alert("Please write something before saving.");
  }
}*/

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

function emotionalRange(){
  const emotionalRange = document.getElementById("emotionalRange");
  if (emotionalRange) {
    fetch('/summaryEmotionRange', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
      console.log('Received emotion range list:', data);
      const emotionArray = Object.entries(data).map(([emotion, count]) => ({
        emotion,
        count
      }));

      // Loop through and create list items
      emotionArray.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.emotion}: ${item.count}`;
        emotionalRange.appendChild(li);
      });
    })
    // .then(data => {
    //   historyList.innerHTML = "";
    //   data.forEach(entry => {
    //     const li = document.createElement("li");
    //     li.textContent = `${entry.date}: ${entry.content.substring(0, 30)}...`;
    //     li.onclick = () => showDetailedEntry(entry);
    //     emotionalRange.appendChild(li);
    //   });
    // })
    .catch(error => console.error('Error:', error));
  }
}

function totalEntry(){
  const summaryTotalEntry = document.getElementById("total-entry");
  if (summaryTotalEntry) {
    fetch('/summaryTotalEntry', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
      console.log('Received Total Input:', data);
      summaryTotalEntry.innerHTML = '';
      
      const li = document.createElement('li');
      li.textContent = `${data} total days`;
      summaryTotalEntry.appendChild(li);
    })
    .catch(error => console.error('Error:', error));
  }
}

function topThemes(){
  const topThemes = document.getElementById("top-themes");
  if (topThemes) {
    fetch('/summaryTop3Themes', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
      console.log('Received top themes:', data);
      const themes = Object.entries(data).map(([theme]) => ({
        theme
      }));

      // Loop through and create list items
      themes.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.theme}`;
        topThemes.appendChild(li);
      });
    })
    .catch(error => console.error('Error:', error));
  }
}

function longestStreak(){
  const summaryStreak = document.getElementById("input-streak");
  if (summaryStreak) {
    fetch('/summaryInputStreak', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
      console.log('Received Input Streak:', data);
      summaryStreak.innerHTML = '';
      
      const li = document.createElement('li');
      li.textContent = `${data} days in a row`;
      summaryStreak.appendChild(li);
    })
    .catch(error => console.error('Error:', error));
  }

}

function journalHistoryList(){
  const journalHistory = document.getElementById('weekly-day');
  fetch('/journalList')
    .then(response => response.json())
    .then(data => {
      
      journalHistory.innerHTML = '';
      data.forEach(item => {
        const li = document.createElement('li');
        //li.textContent = `Date: ${item.created_time}:<br>Entry: ${item.journal_input}`;
        li.innerHTML = `<b>${item.created_time}</b><br><br>${item.journal_input}`;

        li.dataset.id = item.id;
        li.style.cursor = 'pointer';
        li.addEventListener('click', () => {
          const entryId = li.dataset.id;
          window.location.href = `/result?id=${entryId}`;
          //window.location.href = `/journalDetail/${entryId}`;
        });

        journalHistory.appendChild(li);
      });
    })
    .catch(error => console.error('Error loading history:', error));
}

function getJournalIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

function journalDetail(){
  const journalId = getJournalIdFromUrl();
  if (journalId) {
    fetch(`/journalDetail/${journalId}`)
      .then(res => res.json())
      .then(data => {
        document.getElementById('input-text').textContent = data.journal_input || "No input available.";

        if (data.scores && data.scores.length > 0) {
          const scoreText = data.scores
            .map(score => `${score.score_type}: ${score.severity} (${score.total_score})`)
            .join(', ');
          document.getElementById('score-text').textContent = scoreText;
        } else {
          document.getElementById('score-text').textContent = "No scores available.";
        }

        if (data.emotions && data.emotions.length > 0) {
          document.getElementById('emotions-text').textContent = data.emotions.join(', ');
        } else {
          document.getElementById('emotions-text').textContent = "No emotions recorded.";
        }

        document.getElementById('feedback-text').textContent = data.feedback || "No feedback available.";

        if (data.themes && data.themes.length > 0) {
          document.getElementById('themes-text').textContent = data.themes.join(', ');
        } else {
          document.getElementById('themes-text').textContent = "No themes available.";
        }
      })
      .catch(err => console.error(err));
  } else {
    document.body.textContent = 'No journal id provided.';
  }
}

function historyButtonOnClick(){
  const historyButton = document.getElementById('history-button');
  if (historyButton) {
    historyButton.addEventListener('click', () => {
      window.location.href = '/history';
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {

  /*const saveBtn = document.getElementById("saveButton");
  if (saveBtn) {
    saveBtn.addEventListener("click", saveJournalEntry);
  }*/

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

  historyButtonOnClick();
});

document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;
  emotionalRange();
  totalEntry();
  topThemes();
  longestStreak();

  journalHistoryList();
  if(path==='/result'){
    journalDetail();
  }
  
});

document.addEventListener('DOMContentLoaded', function () {
  const saveButton = document.getElementById('saveButton');
  if (saveButton) {
    saveButton.addEventListener('click', function () {
      const journalText = document.getElementById('journalInput').value.trim();
      
      fetch('/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: journalText }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === "success") {
            document.getElementById("journalInput").value = "";
            window.location.href = `/result?id=${data.journal_id}`;
          } else {
            alert("Failed to save journal entry.");
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert("Error saving journal entry.");
        });
    });
  } else {
    console.error("Element with ID 'saveButton' not found.");
  }
});
