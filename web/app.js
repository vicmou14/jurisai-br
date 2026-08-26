const apiBase = window.JURISAI_API_BASE || "";
const apiKey = sessionStorage.getItem("jurisai_api_key");
if (!apiKey) location.href = "login.html";

async function request(path, options = {}) {
  const headers = {"X-API-Key": apiKey, ...(options.headers || {})};
  if (!(options.body instanceof FormData)) headers["Content-Type"] = "application/json";
  const response = await fetch(apiBase + path, {...options, headers});
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : `Erro ${response.status}`);
  return data;
}

const results = document.querySelector("#results");
const status = document.querySelector("#status");
const historyRoot = document.querySelector("#history");
const historyKey = "jurisai_research_history";

function loadHistory() {
  try { return JSON.parse(sessionStorage.getItem(historyKey) || "[]"); }
  catch { return []; }
}
function saveHistory(items) { sessionStorage.setItem(historyKey, JSON.stringify(items.slice(0, 20))); }
function renderHistory() {
  const items = loadHistory();
  historyRoot.innerHTML = "";
  if (!items.length) { historyRoot.textContent = "Nenhuma pesquisa nesta sessão."; return; }
  items.forEach(item => {
    const article = document.createElement("article");
    article.innerHTML = `<h3>${item.question}</h3><small>${item.grounded ? "Fundamentada" : "Requer revisão humana"} · ${item.sourceCount} fonte(s)</small>`;
    historyRoot.appendChild(article);
  });
}
function renderResearch(data) {
  const root = document.querySelector("#research-result");
  root.innerHTML = "";
  const badge = document.createElement("p");
  badge.className = data.grounded ? "badge grounded" : "badge review";
  badge.textContent = data.grounded ? "Resposta com fontes recuperadas" : "Pesquisa requer revisão humana";
  root.appendChild(badge);
  const answer = document.createElement("p"); answer.textContent = data.answer || "Sem resposta."; root.appendChild(answer);
  const meta = document.createElement("small"); meta.textContent = `${data.quality_reason || ""} · Área: ${data.area || "não classificada"} · Fontes: ${data.source_count || 0}`; root.appendChild(meta);
  if (data.sources?.length) {
    const list = document.createElement("div"); list.innerHTML = "<h3>Fontes recuperadas</h3>";
    data.sources.forEach(source => { const item = document.createElement("article"); item.innerHTML = `<strong>${source.title || "Fonte"}</strong><p>${source.content || source.summary || ""}</p><small>${source.source || ""}</small>`; list.appendChild(item); });
    root.appendChild(list);
  }
  const disclaimer = document.createElement("p"); disclaimer.className = "disclaimer"; disclaimer.textContent = data.disclaimer || "A resposta deve ser revisada antes de qualquer uso profissional."; root.appendChild(disclaimer);
}

document.querySelector("#logout").addEventListener("click", () => { sessionStorage.removeItem("jurisai_api_key"); location.href = "login.html"; });
document.querySelector("#clear-history").addEventListener("click", () => { sessionStorage.removeItem(historyKey); renderHistory(); });

document.querySelector("#research-form").addEventListener("submit", async e => {
  e.preventDefault();
  const status = document.querySelector("#research-status");
  status.textContent = "Pesquisando fontes e avaliando fundamentação...";
  try {
    const question = document.querySelector("#research-question").value;
    const context = document.querySelector("#research-context").value;
    const data = await request("/v1/legal-research", {method: "POST", body: JSON.stringify({question, context})});
    renderResearch(data);
    const history = loadHistory(); history.unshift({question, grounded: !!data.grounded, sourceCount: data.source_count || 0}); saveHistory(history); renderHistory();
    status.textContent = "Pesquisa concluída.";
  } catch (error) { status.textContent = error.message; }
});

document.querySelector("#search-form").addEventListener("submit", async e => {
  e.preventDefault(); status.textContent = "Pesquisando..."; results.innerHTML = "";
  try {
    const data = await request(`/v1/search?query=${encodeURIComponent(document.querySelector("#query").value)}`);
    status.textContent = `${data.results.length} resultado(s)`;
    data.results.forEach(item => { const article = document.createElement("article"); article.innerHTML = `<h3>${item.title}</h3><p>${item.content.slice(0, 1200)}</p><small>Fonte: ${item.source} · Categoria: ${item.category} · Relevância: ${item.score}</small>`; results.appendChild(article); });
  } catch (error) { status.textContent = error.message; }
});

document.querySelector("#document-form").addEventListener("submit", async e => {
  e.preventDefault();
  try {
    const data = await request("/v1/documents", {method: "POST", body: JSON.stringify({title: document.querySelector("#title").value, source: document.querySelector("#source").value, category: document.querySelector("#category").value, content: document.querySelector("#content").value})});
    status.textContent = `Documento salvo: ${data.id}`;
  } catch (error) { status.textContent = error.message; }
});

document.querySelector("#upload-form").addEventListener("submit", async e => {
  e.preventDefault(); const form = new FormData();
  form.append("file", document.querySelector("#file").files[0]); form.append("title", document.querySelector("#upload-title").value); form.append("source", document.querySelector("#upload-source").value);
  try { const data = await request("/v1/documents/upload", {method: "POST", body: form}); status.textContent = `Arquivo processado: ${data.title} (${data.characters} caracteres)`; }
  catch (error) { status.textContent = error.message; }
});

request("/v1/sources").then(data => {
  const root = document.querySelector("#sources"); root.innerHTML = "";
  Object.entries(data).forEach(([group, items]) => { const block = document.createElement("div"); block.innerHTML = `<h3>${group}</h3>`; (items || []).forEach(item => { const p = document.createElement("p"); p.textContent = `${item.name}: ${item.purpose || item.url}`; block.appendChild(p); }); root.appendChild(block); });
}).catch(() => { document.querySelector("#sources").textContent = "Indisponível"; });
renderHistory();
