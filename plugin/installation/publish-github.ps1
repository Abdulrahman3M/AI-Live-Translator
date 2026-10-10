# Publish this extracted project from PowerShell. Defaults to PRIVATE.
# Requires Git and GitHub CLI ('gh') already authenticated to your account.
# Review the repository and files before running; this script creates a new remote repository.
param(
    [string]$Owner = 'Abdulrahman3M',
    [string]$Name = 'AI-Live-Translator',
    [switch]$Public
)
$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..\..'))
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw 'Install GitHub CLI (gh) first.' }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Install Git first.' }
& gh auth status
if ($LASTEXITCODE -ne 0) { throw 'Log in using: gh auth login' }
& gh repo view "$Owner/$Name" --json name *> $null
if ($LASTEXITCODE -eq 0) { throw "Repository $Owner/$Name exists; refusing to overwrite or republish." }
if (-not (Test-Path '.git')) { & git init -b main; if ($LASTEXITCODE -ne 0) { throw 'git init failed' } }
& git add .
if ($LASTEXITCODE -ne 0) { throw 'git add failed' }
& git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { & git commit -m 'feat: initial AI Live Translator v1.0.0'; if ($LASTEXITCODE -ne 0) { throw 'git commit failed (configure git identity)' } }
$visibility = if ($Public) { '--public' } else { '--private' }
& gh repo create "$Owner/$Name" $visibility --source . --remote origin --push
if ($LASTEXITCODE -ne 0) { throw 'GitHub repository creation or push failed.' }
Write-Host "Published https://github.com/$Owner/$Name"
