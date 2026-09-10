<#
CPRIS Skills 版本自检脚本（智能体在使用 cpris-skills 前执行，幂等、不阻塞）

判定逻辑（调用方只需识别输出行前缀，所有分支退出码均为 0）：
  SKIP     距上次联网检查不足 TTL 秒（默认 4 小时），直接用本地版本
  LATEST   远程 main 与本地 HEAD 一致，无需更新
  UPDATED  远程有更新，已 git pull --ff-only；随后输出 SYNCED 表示已同步本机安装目录
  OUTDATED 当前目录不是 git 克隆且远程 VERSION 更新，需手动重新拉取或复制
  WARN     网络或 git 异常，忽略并继续用本地版本，不要立即重试阻塞调用

用法：
  powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_update.ps1 [-TtlSeconds 14400] [-Force]

速度保障：TTL 节流（窗口内不联网）+ http.lowSpeed 5 秒低速超时 + GIT_TERMINAL_PROMPT=0
禁止交互式凭据提示，离线或网络异常时零阻塞直接放行。

仓库根目录解析顺序：-RepoPath 参数 > CPRIS_SKILLS_REPO 环境变量 > 从脚本位置向上找 .git
> C:\work\javacode\cpris_skills（本机主仓库）。
同步目标解析顺序：-SyncDest 参数 > CPRIS_SKILLS_INSTALL 环境变量
> C:\Users\15857\.zcode\skills\cpris-skills（存在才启用同步）。
#>
param(
    [int]$TtlSeconds = 14400,
    [switch]$Force,
    [string]$RepoPath,
    [string]$SyncDest
)

$ErrorActionPreference = 'Continue'

# --- 解析仓库根目录与同步目标 ---
if (-not $RepoPath) { $RepoPath = $env:CPRIS_SKILLS_REPO }
if (-not $RepoPath) {
    $p = Split-Path -Parent $PSScriptRoot
    while ($p -and -not (Test-Path (Join-Path $p '.git'))) {
        $parent = Split-Path -Parent $p
        if (-not $parent -or $parent -eq $p) { $p = $null; break }
        $p = $parent
    }
    if ($p) { $RepoPath = $p }
}
if (-not $RepoPath -and (Test-Path 'C:\work\javacode\cpris_skills\.git')) { $RepoPath = 'C:\work\javacode\cpris_skills' }
if (-not $RepoPath) { $RepoPath = Split-Path -Parent $PSScriptRoot }

if (-not $SyncDest) { $SyncDest = $env:CPRIS_SKILLS_INSTALL }
if (-not $SyncDest -and (Test-Path 'C:\Users\15857\.zcode\skills\cpris-skills')) { $SyncDest = 'C:\Users\15857\.zcode\skills\cpris-skills' }

$gitMode = Test-Path (Join-Path $RepoPath '.git')
$marker = if ($gitMode) { Join-Path $RepoPath '.git\cpris_last_check' } else { Join-Path $RepoPath '.cpris_last_check' }
function Touch-Marker {
    try { Set-Content -Path $marker -Value (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss') -Encoding ASCII } catch { }
}

# --- TTL 节流：窗口内不联网，直接跳过（不刷新标记，避免反复顺延窗口） ---
if (-not $Force -and (Test-Path $marker)) {
    try {
        if (((Get-Date) - (Get-Item $marker).LastWriteTime).TotalSeconds -lt $TtlSeconds) {
            Write-Output "SKIP: 距上次联网检查不足 $TtlSeconds 秒，直接使用本地版本。"
            exit 0
        }
    } catch { }
}

# --- git 克隆模式：SHA 对比 + 自动 pull + 同步安装目录 ---
if ($gitMode) {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Output 'WARN: 未安装 git，跳过更新检查，使用本地版本。'
        Touch-Marker
        exit 0
    }

    $env:GIT_TERMINAL_PROMPT = '0'
    $localSha = (git -C $RepoPath rev-parse HEAD 2>$null)
    $remoteLine = (git -c http.lowSpeedLimit=1 -c http.lowSpeedTime=5 -C $RepoPath ls-remote gitee refs/heads/main 2>$null)
    $remoteSha = if ($remoteLine) { ($remoteLine | Select-Object -First 1) -replace '\s.*$', '' } else { $null }

    if (-not $remoteSha) {
        Write-Output 'WARN: 无法访问 gitee 远程（可能离线或缺少凭据），继续使用本地版本。'
        Touch-Marker
        exit 0
    }
    if ($remoteSha -eq "$localSha".Trim()) {
        Write-Output ('LATEST: 已是最新版本（commit {0}）。' -f "$localSha".Trim().Substring(0, 7))
        Touch-Marker
        exit 0
    }

    $pullOut = git -c http.lowSpeedLimit=1 -c http.lowSpeedTime=5 -C $RepoPath pull --ff-only gitee main 2>&1
    if ($LASTEXITCODE -ne 0) {
        $detail = ($pullOut | Select-Object -First 3) -join ' | '
        Write-Output "WARN: 拉取更新失败（本地可能有未提交修改或历史分叉），继续使用本地版本。$detail"
        Touch-Marker
        exit 0
    }

    $newLog = (git -C $RepoPath log ORIG_HEAD..HEAD --format='%h %s' 2>$null | Where-Object { $_ }) -join '; '
    if (-not $newLog) { $newLog = (git -C $RepoPath log -1 --format='%h %s' 2>$null) -join '' }
    $versionFile = Join-Path $RepoPath 'VERSION'
    $ver = if (Test-Path $versionFile) { (Get-Content $versionFile -First 1).Trim() } else { '未知版本' }
    Write-Output "UPDATED: 已更新到 $ver（$newLog）。"

    if ($SyncDest) {
        $syncRc = 0
        robocopy $RepoPath $SyncDest VERSION CHANGELOG.md SKILL.md README.md .gitignore /NJH /NJS /NDL /NFL /NP | Out-Null
        if ($LASTEXITCODE -gt $syncRc) { $syncRc = $LASTEXITCODE }
        foreach ($d in @('agents', 'references', 'scripts')) {
            if (Test-Path (Join-Path $RepoPath $d)) {
                robocopy (Join-Path $RepoPath $d) (Join-Path $SyncDest $d) /E /XD __pycache__ local /NJH /NJS /NDL /NFL /NP | Out-Null
                if ($LASTEXITCODE -gt $syncRc) { $syncRc = $LASTEXITCODE }
            }
        }
        if ($syncRc -ge 8) {
            Write-Output "WARN: 仓库已更新，但同步到 $SyncDest 失败（robocopy 退出码 $syncRc），请手动同步。"
        } else {
            Write-Output "SYNCED: 已同步安装目录 $SyncDest。"
        }
    }
    Touch-Marker
    exit 0
}

# --- 非 git 拷贝模式：对比远程 VERSION 原始文件（公开仓库可匿名读取） ---
$versionFile = Join-Path $RepoPath 'VERSION'
$localVer = if (Test-Path $versionFile) { (Get-Content $versionFile -First 1).Trim() } else { '' }
$remoteVer = $null
try {
    $resp = Invoke-WebRequest -UseBasicParsing -TimeoutSec 5 -Uri 'https://gitee.com/min-fan-ge/cpris_skills/raw/main/VERSION'
    $content = if ($resp.Content -is [byte[]]) { [Text.Encoding]::UTF8.GetString($resp.Content) } else { "$($resp.Content)" }
    $remoteVer = (($content -split "`r?`n") | Where-Object { $_ } | Select-Object -First 1).Trim()
} catch { }

if (-not $remoteVer) {
    Write-Output 'WARN: 无法获取远程 VERSION（可能离线或仓库私有），继续使用本地版本。'
    Touch-Marker
    exit 0
}
if ($remoteVer -eq $localVer) {
    Write-Output "LATEST: 已是最新版本（$localVer）。"
} else {
    Write-Output "OUTDATED: 本地 $localVer，远程 $remoteVer；当前目录不是 git 克隆，无法自动更新，请从 gitee 重新拉取或复制。"
}
Touch-Marker
exit 0
