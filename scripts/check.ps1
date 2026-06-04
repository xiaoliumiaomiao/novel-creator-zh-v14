# Novel Creator ZH V14 — 快速检查脚本 (PowerShell)
# 运行测试 + lint + CLI smoke

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Novel Creator ZH V14 — 质量检查" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 项目根目录
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ProjectRoot
Set-Location $ProjectRoot

# 1. Ruff lint
Write-Host "[1/4] Ruff lint..." -ForegroundColor Yellow
ruff check .
if ($LASTEXITCODE -ne 0) {
    Write-Host "  FAIL: Lint 未通过" -ForegroundColor Red
} else {
    Write-Host "  PASS" -ForegroundColor Green
}
Write-Host ""

# 2. Unit tests
Write-Host "[2/4] Unit tests..." -ForegroundColor Yellow
python -m pytest --tb=short
if ($LASTEXITCODE -ne 0) {
    Write-Host "  FAIL: 测试未通过" -ForegroundColor Red
} else {
    Write-Host "  PASS" -ForegroundColor Green
}
Write-Host ""

# 3. CLI smoke
Write-Host "[3/4] CLI smoke..." -ForegroundColor Yellow
python -m novel_creator.cli --help > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  FAIL: CLI 不可用" -ForegroundColor Red
} else {
    Write-Host "  PASS" -ForegroundColor Green
}
Write-Host ""

# 4. Build
Write-Host "[4/4] Package build..." -ForegroundColor Yellow
python -m build > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  FAIL: 打包失败" -ForegroundColor Red
} else {
    Write-Host "  PASS" -ForegroundColor Green
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " 检查完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
