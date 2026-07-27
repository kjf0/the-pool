(function () {
  const storageKey = "the-pool.backlog.items";
  const fields = {
    id: document.querySelector("#item-id"),
    title: document.querySelector("#item-title"),
    status: document.querySelector("#item-status"),
    priority: document.querySelector("#item-priority"),
    labels: document.querySelector("#item-labels"),
    assignedDev: document.querySelector("#item-assigned"),
    estimatedCodeComplete: document.querySelector("#item-estimate"),
    description: document.querySelector("#item-description")
  };
  const form = document.querySelector("#backlog-form");
  const list = document.querySelector("#backlog-items");
  const report = document.querySelector("#backlog-report");
  const newButton = document.querySelector("#new-item");
  const resetButton = document.querySelector("#reset-data");

  let seedItems = [];
  let items = [];

  async function loadSeedItems() {
    const response = await fetch("backlog-data.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error("Could not load backlog-data.json");
    }
    return response.json();
  }

  function loadStoredItems() {
    const stored = localStorage.getItem(storageKey);
    if (!stored) {
      return null;
    }

    try {
      return JSON.parse(stored);
    } catch {
      return null;
    }
  }

  function saveItems() {
    localStorage.setItem(storageKey, JSON.stringify(items));
  }

  function nextId() {
    return items.reduce((max, item) => Math.max(max, Number(item.id) || 0), 0) + 1;
  }

  function clearForm() {
    form.reset();
    fields.id.value = "";
    fields.status.value = "Not started";
    fields.priority.value = "P0";
    fields.assignedDev.value = "Unassigned";
    fields.estimatedCodeComplete.value = "TBD";
  }

  function fillForm(item) {
    fields.id.value = item.id;
    fields.title.value = item.title;
    fields.status.value = item.status;
    fields.priority.value = item.priority;
    fields.labels.value = item.labels;
    fields.assignedDev.value = item.assignedDev;
    fields.estimatedCodeComplete.value = item.estimatedCodeComplete;
    fields.description.value = item.description;
  }

  function formItem() {
    return {
      id: fields.id.value ? Number(fields.id.value) : nextId(),
      title: fields.title.value.trim(),
      status: fields.status.value,
      priority: fields.priority.value,
      labels: fields.labels.value.trim(),
      assignedDev: fields.assignedDev.value.trim() || "Unassigned",
      estimatedCodeComplete: fields.estimatedCodeComplete.value.trim() || "TBD",
      description: fields.description.value.trim()
    };
  }

  function renderItems() {
    list.innerHTML = "";
    sortedItems().forEach((item) => {
      const article = document.createElement("article");
      article.className = "backlog-item";
      article.innerHTML = `
          <h3>${item.id}. ${escapeHtml(item.title)}</h3>
          <dl>
            <dt>Status</dt><dd>${escapeHtml(item.status)}</dd>
            <dt>Priority</dt><dd>${escapeHtml(item.priority)}</dd>
            <dt>Labels</dt><dd>${escapeHtml(item.labels)}</dd>
            <dt>Assigned</dt><dd>${escapeHtml(item.assignedDev)}</dd>
            <dt>Estimate</dt><dd>${escapeHtml(item.estimatedCodeComplete)}</dd>
          </dl>
          <p>${escapeHtml(item.description)}</p>
          <button type="button" data-edit="${item.id}">Edit</button>
        `;
      list.appendChild(article);
    });
  }

  function renderReport() {
    report.innerHTML = "";
    sortedItems().forEach((item) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${escapeHtml(item.id)}</td>
        <td>${escapeHtml(item.title)}</td>
        <td>${escapeHtml(item.status)}</td>
        <td>${escapeHtml(item.labels)}</td>
        <td>${escapeHtml(item.priority)}</td>
        <td>${escapeHtml(item.assignedDev)}</td>
        <td>${escapeHtml(item.estimatedCodeComplete)}</td>
        <td>${escapeHtml(item.description)}</td>
      `;
      report.appendChild(row);
    });
  }

  function renderBacklog() {
    renderReport();
    renderItems();
  }

  function sortedItems() {
    return items.slice().sort((a, b) => Number(a.id) - Number(b.id));
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const item = formItem();
    const index = items.findIndex((existing) => Number(existing.id) === Number(item.id));
    if (index === -1) {
      items.push(item);
    } else {
      items[index] = item;
    }
    saveItems();
    clearForm();
    renderBacklog();
  });

  newButton.addEventListener("click", clearForm);

  resetButton.addEventListener("click", () => {
    items = [...seedItems];
    localStorage.removeItem(storageKey);
    clearForm();
    renderBacklog();
  });

  list.addEventListener("click", (event) => {
    const editButton = event.target.closest("[data-edit]");
    if (!editButton) {
      return;
    }
    const item = items.find((candidate) => Number(candidate.id) === Number(editButton.dataset.edit));
    if (item) {
      fillForm(item);
    }
  });

  loadSeedItems()
    .then((loadedItems) => {
      seedItems = loadedItems;
      items = loadStoredItems() || [...seedItems];
      clearForm();
      renderBacklog();
    })
    .catch((error) => {
      list.textContent = error.message;
    });
})();
