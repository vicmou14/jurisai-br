const apiBase = window.JURISAI_API_BASE || "";
const apiKey = sessionStorage.getItem("jurisai_api_key");
if (!apiKey) location.href = "login.html";

async function request(path, options = {}) {
  const response = await fetch(apiBase + path, {
    headers: { "Content-Type": "application/json", "X-API-Key": apiKey, ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) throw new Error(`Erro ${response.status}`);
  return response.json();
}

const results = document.querySelector("#results");
const status = document.querySelector("#status");

document.querySelector("#search-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = document.querySelector("#query").value;
  status.textContent = "Pesquisando...";
  results.innerHTML = "";
  try {
    const data = await request(`/v1/search?query=${encodeURIComponent(query)}`);
    status.textContent = `${data.results.length} resultado(s)`;
    for (const item of data.results) {
      const article = document.createElement("article");
      article.innerHTML = `<h3>${item.title}</h3><p>${item.content}</p><small>Fonte: ${item.source} | Relevância: ${item.score}</small>`;
      results.appendChild(article);
    }
  } catch (error) { status.textContent = error.message; }
});

document.querySelector("#document-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = { title: title.value, source: source.value, category: category.value, content: content.value };
  try {
    const data = await request("/v1/documents", { method: "POST", body: JSON.stringify(payload) });
    status.textContent = `Documento salvo: ${data.id}`;
  } catch (error) { status.textContent = error.message; }
});
