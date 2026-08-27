$ErrorActionPreference = 'Stop'

Write-Host 'JurisAI-BR - inicialização local' -ForegroundColor Cyan

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    throw 'Ollama não encontrado. Instale-o antes de continuar.'
}

$model = $env:JURISAI_OLLAMA_MODEL
if ([string]::IsNullOrWhiteSpace($model)) { $model = 'qwen3:8b' }

$installedModels = (ollama list | Out-String)
if ($installedModels -notmatch [regex]::Escape($model)) {
    throw "O modelo $model não está instalado. Execute: ollama pull $model"
}

if (-not (Test-Path '.venv')) {
    py -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

if (-not (Test-Path '.env')) {
    Copy-Item .env.example .env
}

$env:JURISAI_TEXT_PROVIDER = 'ollama'
$env:JURISAI_OLLAMA_URL = 'http://127.0.0.1:11434'
$env:JURISAI_OLLAMA_MODEL = $model

Write-Host "Ollama: $model" -ForegroundColor Green
Write-Host 'Iniciando JurisAI-BR em http://127.0.0.1:8000/web/' -ForegroundColor Green

Start-Process 'http://127.0.0.1:8000/web/'
uvicorn app.main:app --reload
