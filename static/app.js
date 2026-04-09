const state = {
  tasks: [],
  filter: "all",
  loading: true,
};

const elements = {
  form: document.querySelector("#task-form"),
  title: document.querySelector("#title"),
  feedback: document.querySelector("#feedback"),
  error: document.querySelector("#error"),
  loading: document.querySelector("#loading"),
  list: document.querySelector("#task-list"),
  summary: document.querySelector("#summary"),
  filters: document.querySelectorAll(".filter-button"),
  emptyState: document.querySelector("#empty-state"),
};

function setFeedback(message = "") {
  elements.feedback.textContent = message;
}

function setError(message = "") {
  elements.error.textContent = message;
}

function formatDate(isoString) {
  return new Date(isoString).toLocaleString(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function getVisibleTasks() {
  if (state.filter === "active") {
    return state.tasks.filter((task) => !task.completed);
  }

  if (state.filter === "completed") {
    return state.tasks.filter((task) => task.completed);
  }

  return state.tasks;
}

function render() {
  const visibleTasks = getVisibleTasks();
  const remaining = state.tasks.filter((task) => !task.completed).length;

  elements.loading.hidden = !state.loading;
  elements.list.innerHTML = "";
  elements.summary.textContent = `${state.tasks.length} total tasks, ${remaining} remaining`;

  elements.filters.forEach((button) => {
    button.classList.toggle("active", button.dataset.filter === state.filter);
  });

  if (!state.loading && visibleTasks.length === 0) {
    elements.list.appendChild(elements.emptyState.content.cloneNode(true));
    return;
  }

  visibleTasks.forEach((task) => {
    const item = document.createElement("li");
    item.className = `task-item${task.completed ? " completed" : ""}`;

    const toggle = document.createElement("input");
    toggle.type = "checkbox";
    toggle.className = "task-toggle";
    toggle.checked = task.completed;
    toggle.setAttribute("aria-label", `Mark ${task.title} as completed`);
    toggle.addEventListener("change", () => updateTask(task.id, toggle.checked));

    const content = document.createElement("div");
    content.className = "task-content";

    const title = document.createElement("p");
    title.className = "task-title";
    title.textContent = task.title;

    const date = document.createElement("p");
    date.className = "task-date";
    date.textContent = `Created ${formatDate(task.createdAt)}`;

    content.append(title, date);

    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "task-action";
    removeButton.textContent = "Delete";
    removeButton.addEventListener("click", () => deleteTask(task.id));

    item.append(toggle, content, removeButton);
    elements.list.appendChild(item);
  });
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  let payload;
  try {
    payload = await response.json();
  } catch (error) {
    throw new Error("The server returned an unexpected response.");
  }

  if (!response.ok) {
    throw new Error(payload.error || "Something went wrong.");
  }

  return payload.data;
}

async function loadTasks() {
  state.loading = true;
  setError();
  render();

  try {
    state.tasks = await request("/tasks");
  } catch (error) {
    setError(error.message);
  } finally {
    state.loading = false;
    render();
  }
}

async function createTask(event) {
  event.preventDefault();
  setFeedback();
  setError();

  const title = elements.title.value.trim();
  if (!title) {
    setError("Please enter a task title.");
    return;
  }

  try {
    const task = await request("/tasks", {
      method: "POST",
      body: JSON.stringify({ title }),
    });
    state.tasks = [task, ...state.tasks];
    elements.form.reset();
    setFeedback("Task added.");
    render();
  } catch (error) {
    setError(error.message);
  }
}

async function updateTask(taskId, completed) {
  setFeedback();
  setError();

  try {
    const updatedTask = await request(`/tasks/${taskId}`, {
      method: "PATCH",
      body: JSON.stringify({ completed }),
    });
    state.tasks = state.tasks.map((task) => (task.id === taskId ? updatedTask : task));
    setFeedback(completed ? "Task marked as completed." : "Task marked as active.");
    render();
  } catch (error) {
    setError(error.message);
    await loadTasks();
  }
}

async function deleteTask(taskId) {
  setFeedback();
  setError();

  try {
    await request(`/tasks/${taskId}`, {
      method: "DELETE",
    });
    state.tasks = state.tasks.filter((task) => task.id !== taskId);
    setFeedback("Task deleted.");
    render();
  } catch (error) {
    setError(error.message);
  }
}

elements.form.addEventListener("submit", createTask);

elements.filters.forEach((button) => {
  button.addEventListener("click", () => {
    state.filter = button.dataset.filter;
    render();
  });
});

loadTasks();
