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
  const newButton = document.querySelector("#new-item");
  const resetButton = document.querySelector("#reset-data");

  let items = loadItems();

  function loadItems() {
    const stored = localStorage.getItem(storageKey);
    if (!stored) {
      return [...window.initialBacklogItems];
    }

    try {
      return JSON.parse(stored);
    } catch {
      return [...window.initialBacklogItems];
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
    items
      .slice()
      .sort((a, b) => Number(a.id) - Number(b.id))
      .forEach((item) => {
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
    renderItems();
  });

  newButton.addEventListener("click", clearForm);

  resetButton.addEventListener("click", () => {
    items = [...window.initialBacklogItems];
    saveItems();
    clearForm();
    renderItems();
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

  clearForm();
  renderItems();
})();
