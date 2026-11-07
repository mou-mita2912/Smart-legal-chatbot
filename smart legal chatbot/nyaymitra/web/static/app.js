// NyayMitra Interactive Frontend Controller

document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const jurisdictionSelect = document.getElementById('jurisdiction-select');
  const aiStatusText = document.getElementById('ai-status-text');
  const navTabs = document.querySelectorAll('.nav-tab');
  const tabPanes = document.querySelectorAll('.tab-pane');

  // Modal Elements
  const settingsModal = document.getElementById('settings-modal');
  const openSettingsBtn = document.getElementById('open-settings-btn');
  const closeModalBtn = document.getElementById('close-modal-btn');
  const saveSettingsBtn = document.getElementById('save-settings-btn');
  const geminiKeyInput = document.getElementById('gemini-key-input');
  const modalKeyStatus = document.getElementById('modal-key-status');

  // Chat Elements
  const chatMessages = document.getElementById('chat-messages');
  const chatInput = document.getElementById('chat-input');
  const chatSendBtn = document.getElementById('chat-send-btn');

  // Contract Elements
  const contractText = document.getElementById('contract-text');
  const contractRole = document.getElementById('contract-role');
  const runContractReviewBtn = document.getElementById('run-contract-review-btn');
  const contractOutputCard = document.getElementById('contract-output-card');
  const contractOutput = document.getElementById('contract-output');
  const loadSampleContractBtn = document.getElementById('load-sample-contract');

  // IRAC Elements
  const iracScenario = document.getElementById('irac-scenario');
  const runIracBtn = document.getElementById('run-irac-btn');
  const iracOutputCard = document.getElementById('irac-output-card');
  const iracOutput = document.getElementById('irac-output');
  const loadSampleIracBtn = document.getElementById('load-sample-irac');

  // Drafter Elements
  const draftDocType = document.getElementById('draft-doc-type');
  const draftPartyA = document.getElementById('draft-party-a');
  const draftPartyB = document.getElementById('draft-party-b');
  const draftPurpose = document.getElementById('draft-purpose');
  const draftDemands = document.getElementById('draft-demands');
  const runDraftBtn = document.getElementById('run-draft-btn');
  const draftOutputCard = document.getElementById('draft-output-card');
  const draftOutput = document.getElementById('draft-output');
  const downloadDraftBtn = document.getElementById('download-draft-btn');

  // Procedures Elements
  const procButtons = document.querySelectorAll('.proc-btn');
  const procedureOutput = document.getElementById('procedure-output');

  // Converter Elements
  const bnsSearchInput = document.getElementById('bns-search-input');
  const bnsSearchBtn = document.getElementById('bns-search-btn');
  const converterOutputCard = document.getElementById('converter-output-card');
  const converterOutput = document.getElementById('converter-output');
  const chips = document.querySelectorAll('.chip');

  // Check initial API status
  checkStatus();

  // Navigation Tab Switching
  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      navTabs.forEach(t => t.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));

      tab.classList.add('active');
      const targetPane = document.getElementById(tab.dataset.tab);
      if (targetPane) targetPane.classList.add('active');

      if (tab.dataset.tab === 'procedures-tab' && !procedureOutput.dataset.loaded) {
        loadProcedure('rti');
      }
    });
  });

  // Modal Handlers
  openSettingsBtn.addEventListener('click', () => {
    settingsModal.classList.remove('hidden');
    checkStatus();
  });

  closeModalBtn.addEventListener('click', () => {
    settingsModal.classList.add('hidden');
  });

  saveSettingsBtn.addEventListener('click', async () => {
    const key = geminiKeyInput.value.trim();
    if (!key) return;
    try {
      const res = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ gemini_api_key: key })
      });
      const data = await res.json();
      if (data.has_gemini_key) {
        aiStatusText.textContent = "Gemini AI Active";
        modalKeyStatus.textContent = "✅ Connected to Google Gemini API";
        modalKeyStatus.style.color = "var(--success-green)";
        setTimeout(() => settingsModal.classList.add('hidden'), 1000);
      }
    } catch (e) {
      modalKeyStatus.textContent = "❌ Failed to save key.";
    }
  });

  async function checkStatus() {
    try {
      const res = await fetch('/api/status');
      const data = await res.json();
      if (data.has_gemini_key) {
        aiStatusText.textContent = "Gemini AI Active";
        modalKeyStatus.textContent = "Google Gemini API key is configured.";
      } else {
        aiStatusText.textContent = "Local Knowledge Engine";
        modalKeyStatus.textContent = "Running in Local Offline Mode. Add key for generative AI.";
      }
    } catch (e) {
      aiStatusText.textContent = "Local Engine";
    }
  }

  // Markdown-to-HTML parser (lightweight)
  function renderMarkdown(md) {
    if (!md) return '';
    let html = md
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
      .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/gim, '<em>$1</em>')
      .replace(/`([^`]+)`/gim, '<code>$1</code>')
      .replace(/~~(.*?)~~/gim, '<del>$1</del>')
      .replace(/\n\n/gim, '<p></p>')
      .replace(/^\s*\-\s(.*$)/gim, '<li>$1</li>')
      .replace(/^\s*\d+\.\s(.*$)/gim, '<li>$1</li>');

    // Wrap list items
    html = html.replace(/(<li>.*<\/li>)/gim, '<ul>$1</ul>');
    return html;
  }

  // --- 1. CHAT FUNCTIONALITY ---
  async function sendChatMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    // Append user message
    appendMessage('user', text);
    chatInput.value = '';

    // Append assistant typing indicator
    const typingId = appendMessage('assistant', '<em>NyayMitra is analyzing legal provisions...</em>');

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          jurisdiction: jurisdictionSelect.value
        })
      });
      const data = await res.json();
      updateMessage(typingId, data.response);
    } catch (err) {
      updateMessage(typingId, "An error occurred while contacting NyayMitra service.");
    }
  }

  function appendMessage(sender, text) {
    const msgId = 'msg-' + Date.now();
    const div = document.createElement('div');
    div.id = msgId;
    div.className = `message ${sender}-message`;

    if (sender === 'assistant') {
      div.innerHTML = `
        <div class="message-header">
          <span class="avatar">⚖️</span>
          <strong>NyayMitra Assistant</strong>
        </div>
        <div class="message-body markdown-body">${renderMarkdown(text)}</div>
      `;
    } else {
      div.innerHTML = `
        <div class="message-body">${escapeHtml(text)}</div>
      `;
    }

    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return msgId;
  }

  function updateMessage(msgId, text) {
    const el = document.getElementById(msgId);
    if (el) {
      const body = el.querySelector('.message-body');
      if (body) {
        body.innerHTML = renderMarkdown(text);
      }
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }

  function escapeHtml(unsafe) {
    return unsafe
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  chatSendBtn.addEventListener('click', sendChatMessage);
  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendChatMessage();
    }
  });

  // --- 2. CONTRACT RISK REVIEW ---
  loadSampleContractBtn.addEventListener('click', () => {
    contractText.value = `SECTION 8. INDEMNIFICATION AND LIABILITY
8.1 Client agrees to defend, indemnify, and hold harmless Service Provider and its affiliates from and against any and all losses, damages, liabilities, costs, and expenses (including attorneys' fees) arising out of or related to this Agreement.
8.2 In no event shall Service Provider's total aggregate liability under this Agreement exceed the fees paid by Client in the one (1) month prior to the event giving rise to liability. Service Provider shall have sole discretion to terminate this Agreement immediately upon written notice without cause.
8.3 Client agrees not to engage, employ, or contract with any competitor of Service Provider for a period of twenty-four (24) months post-termination anywhere globally.`;
  });

  runContractReviewBtn.addEventListener('click', async () => {
    const text = contractText.value.trim();
    if (!text) {
      alert("Please enter or paste contract clauses to review.");
      return;
    }

    runContractReviewBtn.textContent = "Analyzing Clauses...";
    runContractReviewBtn.disabled = true;

    try {
      const res = await fetch('/api/contract-review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contract_text: text,
          jurisdiction: jurisdictionSelect.value,
          party_role: contractRole.value
        })
      });
      const data = await res.json();
      contractOutput.innerHTML = renderMarkdown(data.result);
      contractOutputCard.classList.remove('hidden');
    } catch (e) {
      alert("Error reviewing contract.");
    } finally {
      runContractReviewBtn.textContent = "Perform Risk Analysis";
      runContractReviewBtn.disabled = false;
    }
  });

  // --- 3. IRAC ANALYZER ---
  loadSampleIracBtn.addEventListener('click', () => {
    iracScenario.value = `Employee 'A' has worked as a senior software architect for a tech company in London for 3 years with continuous clean reviews. 
Last Monday, 'A' raised internal concerns regarding workplace safety and non-payment of agreed overtime. 
The following morning, the employer called 'A' into an unscheduled 10-minute meeting, informed 'A' that their role was redundant with immediate effect, and blocked their building access and email accounts without offering any redundancy consultation, alternative employment, or right of appeal.`;
    jurisdictionSelect.value = "United Kingdom (England & Wales)";
  });

  runIracBtn.addEventListener('click', async () => {
    const text = iracScenario.value.trim();
    if (!text) {
      alert("Please enter a factual scenario.");
      return;
    }

    runIracBtn.textContent = "Generating IRAC Analysis...";
    runIracBtn.disabled = true;

    try {
      const res = await fetch('/api/irac', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scenario: text,
          jurisdiction: jurisdictionSelect.value
        })
      });
      const data = await res.json();
      iracOutput.innerHTML = renderMarkdown(data.result);
      iracOutputCard.classList.remove('hidden');
    } catch (e) {
      alert("Error generating IRAC assessment.");
    } finally {
      runIracBtn.textContent = "Generate IRAC Assessment";
      runIracBtn.disabled = false;
    }
  });

  // --- 4. DOCUMENT DRAFTER ---
  runDraftBtn.addEventListener('click', async () => {
    const payload = {
      doc_type: draftDocType.value,
      party_a: draftPartyA.value.trim() || "[First Party / Sender]",
      party_b: draftPartyB.value.trim() || "[Second Party / Recipient]",
      purpose_dispute: draftPurpose.value.trim() || "[Dispute / Commercial Purpose]",
      governing_law: jurisdictionSelect.value,
      demands_terms: draftDemands.value.trim() || "[Specific Demands or Terms]"
    };

    runDraftBtn.textContent = "Generating Instrument...";
    runDraftBtn.disabled = true;

    try {
      const res = await fetch('/api/draft', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      draftOutput.dataset.raw = data.draft;
      draftOutput.innerHTML = renderMarkdown(data.draft);
      draftOutputCard.classList.remove('hidden');
    } catch (e) {
      alert("Error generating legal draft.");
    } finally {
      runDraftBtn.textContent = "Generate Legal Draft";
      runDraftBtn.disabled = false;
    }
  });

  downloadDraftBtn.addEventListener('click', () => {
    const raw = draftOutput.dataset.raw || draftOutput.innerText;
    const blob = new Blob([raw], { type: 'text/plain;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${draftDocType.value.replace(/[^a-zA-Z0-9]/g, '_')}_Draft.txt`;
    link.click();
  });

  // --- 5. PROCEDURAL GUIDES ---
  procButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      procButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      loadProcedure(btn.dataset.proc);
    });
  });

  async function loadProcedure(procKey) {
    procedureOutput.innerHTML = "<em>Loading statutory procedure...</em>";
    try {
      const res = await fetch(`/api/procedure/${procKey}`);
      const data = await res.json();
      if (data.guide) {
        let md = `### ${data.guide.title}\n**Governing Law:** ${data.guide.governing_law}\n\n`;
        data.guide.steps.forEach(s => {
          md += `**Step ${s.step}: ${s.title}**\n${s.details}\n\n`;
        });
        procedureOutput.innerHTML = renderMarkdown(md);
        procedureOutput.dataset.loaded = "true";
      }
    } catch (e) {
      procedureOutput.innerHTML = "Failed to load procedure.";
    }
  }

  // --- 6. IPC ⇄ BNS CONVERTER ---
  async function performBnsLookup(query) {
    if (!query) return;
    try {
      const res = await fetch(`/api/bns-lookup?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      if (data.result && Object.keys(data.result).length > 0) {
        const r = data.result;
        let md = `### ${r.title || 'Statutory Offence'}\n`;
        if (r.ipc) md += `- **Old Code (IPC):** \`${r.ipc}\`\n`;
        if (r.bns) md += `- **New Law (BNS 2023):** \`${r.bns}\`\n`;
        if (r.crpc) md += `- **Old Code (CrPC):** \`${r.crpc}\`\n`;
        if (r.bnss) md += `- **New Law (BNSS 2023):** \`${r.bnss}\`\n`;
        if (r.punishment) md += `- **Prescribed Punishment:** ${r.punishment}\n`;
        if (r.notes) md += `- **Key Reform:** ${r.notes}\n`;
        if (r.highlights) md += `- **Key Highlight:** ${r.highlights}\n`;
        converterOutput.innerHTML = renderMarkdown(md);
      } else {
        converterOutput.innerHTML = `<p>No direct cross-reference found for section <code>${escapeHtml(query)}</code>. Under our safety guardrails: <em>I cannot verify the exact section for this specific scenario; please consult legal counsel.</em></p>`;
      }
      converterOutputCard.classList.remove('hidden');
    } catch (e) {
      converterOutput.innerHTML = "Error querying conversion database.";
    }
  }

  bnsSearchBtn.addEventListener('click', () => {
    performBnsLookup(bnsSearchInput.value.trim());
  });

  bnsSearchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      performBnsLookup(bnsSearchInput.value.trim());
    }
  });

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      bnsSearchInput.value = chip.dataset.sec;
      performBnsLookup(chip.dataset.sec);
    });
  });

  // Copy-to-Clipboard Utility
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.dataset.target;
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        const textToCopy = targetEl.dataset.raw || targetEl.innerText;
        navigator.clipboard.writeText(textToCopy).then(() => {
          const original = btn.textContent;
          btn.textContent = "Copied! ✓";
          setTimeout(() => btn.textContent = original, 2000);
        });
      }
    });
  });
});

