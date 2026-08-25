document.addEventListener("DOMContentLoaded", () => {
    const textInput = document.getElementById("textInput");
    const analyzeBtn = document.getElementById("analyzeBtn");
  
    // Sections
    const metricsSection = document.getElementById("metricsSection");
    const secondaryGrid = document.getElementById("secondaryGrid");
    const resultsSection = document.getElementById("resultsSection");
  
    // Metrics elements
    const statTokens = document.getElementById("statTokens");
    const statSentences = document.getElementById("statSentences");
    const statNounsVerbs = document.getElementById("statNounsVerbs");
    const sentimentCard = document.getElementById("sentimentCard");
    const sentimentLabel = document.getElementById("sentimentLabel");
    const sentimentPolarity = document.getElementById("sentimentPolarity");
  
    // Badges & Tables
    const compoundsContainer = document.getElementById("compoundsContainer");
    const entitiesContainer = document.getElementById("entitiesContainer");
    const tokensTableBody = document.getElementById("tokensTableBody");
  
    // Preset buttons
    document.querySelectorAll(".btn-preset").forEach(btn => {
      btn.addEventListener("click", () => {
        textInput.value = btn.getAttribute("data-text");
        runAnalysis();
      });
    });
  
    analyzeBtn.addEventListener("click", runAnalysis);
  
    async function runAnalysis() {
      const text = textInput.value.trim();
      if (!text) return;
  
      analyzeBtn.disabled = true;
      analyzeBtn.innerHTML = "Analysieren...";
  
      try {
        const response = await fetch("/api/analyze", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text })
        });
  
        if (!response.ok) {
          throw new Error("Fehler bei der Analyse");
        }
  
        const data = await response.json();
        renderDashboard(data);
      } catch (err) {
        alert("Fehler: " + err.message);
      } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = `<span class="btn-icon">⚡</span> Text analysieren`;
      }
    }
  
    function renderDashboard(data) {
      // Reveal sections
      metricsSection.style.display = "grid";
      secondaryGrid.style.display = "grid";
      resultsSection.style.display = "block";
  
      // 1. Render Statistics
      statTokens.textContent = data.statistics.token_count;
      statSentences.textContent = data.statistics.sentence_count;
      statNounsVerbs.textContent = `${data.statistics.noun_count} / ${data.statistics.verb_count}`;
  
      // 2. Render Sentiment
      sentimentLabel.textContent = data.sentiment.label;
      sentimentPolarity.textContent = `Polarität: ${data.sentiment.polarity} (Subj: ${data.sentiment.subjectivity})`;
      
      sentimentCard.className = "metric-box sentiment-box " + 
        (data.sentiment.label === "Positiv" ? "positive" : data.sentiment.label === "Negativ" ? "negative" : "neutral");
  
      // 3. Render Compound Words
      compoundsContainer.innerHTML = "";
      if (data.compounds && data.compounds.length > 0) {
        data.compounds.forEach(c => {
          const chip = document.createElement("div");
          chip.className = "compound-chip";
          chip.innerHTML = `<strong>${c.original}</strong> → <span class="decomp">${c.components.join(" + ")}</span>`;
          compoundsContainer.appendChild(chip);
        });
      } else {
        compoundsContainer.innerHTML = '<p class="empty-hint">Keine Komposita erkannt.</p>';
      }
  
      // 4. Render Named Entities (NER)
      entitiesContainer.innerHTML = "";
      if (data.entities && data.entities.length > 0) {
        data.entities.forEach(ent => {
          const badge = document.createElement("span");
          badge.className = `ner-badge ${ent.label}`;
          badge.textContent = `${ent.text} (${ent.label})`;
          entitiesContainer.appendChild(badge);
        });
      } else {
        entitiesContainer.innerHTML = '<p class="empty-hint">Keine benannten Entitäten identifiziert.</p>';
      }
  
      // 5. Render Morphosyntactic Table
      tokensTableBody.innerHTML = "";
      data.tokens.forEach(tok => {
        const tr = document.createElement("tr");
  
        const posClass = ["NOUN", "VERB", "ADJ", "PROPN"].includes(tok.pos) 
          ? `pos-${tok.pos}` 
          : "pos-OTHER";
  
        tr.innerHTML = `
          <td><strong>${tok.text}</strong></td>
          <td><code>${tok.lemma}</code></td>
          <td><span class="pos-tag ${posClass}">${tok.pos}</span> <small style="color: #64748b">(${tok.tag})</small></td>
          <td>${tok.case !== "N/A" ? tok.case : "—"}</td>
          <td>${tok.gender !== "N/A" ? tok.gender : "—"}</td>
          <td>${tok.number !== "N/A" ? tok.number : "—"}</td>
          <td><code>${tok.dep}</code> <small>(${tok.head})</small></td>
        `;
        tokensTableBody.appendChild(tr);
      });
    }
  });