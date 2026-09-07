# CPRIS AI gateway fallback client for Windows machines without Python.
# Pure ASCII on purpose: Windows PowerShell 5.1 reads BOM-less files as ANSI,
# non-ASCII literals break parsing (see references/known-issues.md).
#
# Usage (from the skill root or any directory, adjust path as needed):
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\cpris_call.ps1 -Method GET -Path /childrenInfo/page -Query current=1
#   powershell ... -Method GET -Path /childrenInfo/page -QueryFile q.txt
#       q.txt: UTF-8 text file, one "key=value" per line; use it when values
#       contain Chinese characters (command-line encoding is unreliable).
#   powershell ... -Method POST -Path /childrenInfo/saveOrUpdate -BodyFile body.json
#       body.json: UTF-8 JSON file (BOM tolerated).
#
# Output: first line "HTTP_STATUS:<code>", then the raw response body.
# NOTE for Git Bash users: prefix the command with MSYS_NO_PATHCONV=1,
# otherwise arguments starting with "/" (like -Path /childrenInfo/page)
# get rewritten into Windows paths by the MSYS layer.

param(
  [Parameter(Mandatory = $true)][ValidateSet('GET', 'POST', 'PUT', 'PATCH')][string]$Method,
  [Parameter(Mandatory = $true)][string]$Path,
  [ValidateSet('test', 'production')][string]$EnvName = 'test',
  [string[]]$Query = @(),
  [string]$QueryFile,
  [string]$Body,
  [string]$BodyFile,
  [int]$TimeoutSec = 30
)

$ErrorActionPreference = 'Stop'

# --- gateway config, located relative to this script (../references) ---
$root = Split-Path -Parent $PSScriptRoot
$configPath = Join-Path $root 'references\gateway-config.json'
if (-not (Test-Path $configPath)) { Write-Error 'gateway-config.json not found'; exit 2 }
$config = Get-Content -Raw $configPath | ConvertFrom-Json
$envInfo = $config.environments.$EnvName
if (-not $envInfo) { Write-Error ('unknown environment: ' + $EnvName); exit 2 }
$gateway = $envInfo.aiGateway

# --- resolve API key: environment variables first, then DPAPI credential file ---
function Get-ApiKey {
  $scoped = [Environment]::GetEnvironmentVariable('CPRIS_' + $EnvName.ToUpper() + '_API_KEY')
  if ($scoped) { return $scoped }
  $generic = [Environment]::GetEnvironmentVariable('CPRIS_API_KEY')
  if ($generic) {
    $bound = [Environment]::GetEnvironmentVariable('CPRIS_API_KEY_GATEWAY')
    if ("$bound".TrimEnd('/') -ne $gateway) { Write-Error 'CPRIS_API_KEY_GATEWAY mismatch'; exit 2 }
    return $generic
  }
  $cfgRoot = [Environment]::GetEnvironmentVariable('CPRIS_CONFIG_HOME')
  if (-not $cfgRoot -or -not [System.IO.Path]::IsPathRooted($cfgRoot)) { $cfgRoot = Join-Path $env:APPDATA 'cpris' }
  $credPath = Join-Path $cfgRoot ('cpris-wxapp-rest-api\' + $EnvName + '\credentials.json')
  if (-not (Test-Path $credPath)) { Write-Error ('credentials not found, run login first: ' + $credPath); exit 2 }
  $cred = Get-Content -Raw $credPath | ConvertFrom-Json
  if ($cred.gateway -ne $gateway -or $cred.environment -ne $EnvName) { Write-Error 'credential environment/gateway mismatch, re-login for this environment'; exit 2 }
  Add-Type -AssemblyName System.Security | Out-Null
  $bytes = [System.Convert]::FromBase64String($cred.apiKeyProtected)
  return [System.Text.Encoding]::UTF8.GetString([System.Security.Cryptography.ProtectedData]::Unprotect(
    $bytes, $null, [System.Security.Cryptography.DataProtectionScope]::CurrentUser))
}
$key = Get-ApiKey

# --- route business path to /ai/gw/<service>/<business> per gateway-config.json ---
if ($Path -notmatch '^/') { $Path = '/' + $Path }
if ($Path -match '[\s\\]' -or $Path -match '%(?![0-9a-fA-F]{2})' -or $Path -match '//') {
  Write-Error 'path contains whitespace, backslash, bad escape or duplicate slash'; exit 2
}
$business = $Path
$service = $null
if ($Path.StartsWith('/ai/gw/')) {
  $rest = $Path.Substring(7)
  $idx = $rest.IndexOf('/')
  if ($idx -lt 1) { Write-Error 'gateway path must contain service and business path'; exit 2 }
  $service = $rest.Substring(0, $idx)
  $business = $rest.Substring($idx)
}
$segment = $business.TrimStart('/').Split('/')[0]
if ($config.blockedPrefixes -contains $segment) { Write-Error ('blocked prefix: ' + $segment); exit 2 }
foreach ($bp in $config.blockedPaths) {
  if ($business -eq $bp -or $business.StartsWith($bp + '/')) { Write-Error ('blocked path: ' + $bp); exit 2 }
}
$expected = $config.prefixToService.$segment
if (-not $expected) { Write-Error ('no service mapping for prefix: ' + $segment); exit 2 }
if ($service -and $service -ne $expected) { Write-Error 'service segment does not match prefix mapping'; exit 2 }
$fullPath = '/ai/gw/' + $expected + $business

# --- query string: inline pairs (ASCII safe) plus UTF-8 file lines "k=v" ---
$pairs = @()
foreach ($kv in $Query) {
  $i = $kv.IndexOf('=')
  if ($i -lt 1) { Write-Error ('bad -Query pair: ' + $kv); exit 2 }
  $pairs += ,@($kv.Substring(0, $i), $kv.Substring($i + 1))
}
if ($QueryFile) {
  foreach ($line in (Get-Content -Encoding UTF8 $QueryFile)) {
    if (-not $line.Trim()) { continue }
    $i = $line.IndexOf('=')
    if ($i -lt 1) { Write-Error ('bad query file line: ' + $line); exit 2 }
    $pairs += ,@($line.Substring(0, $i), $line.Substring($i + 1))
  }
}
if ($pairs.Count -gt 0) {
  $qs = ($pairs | ForEach-Object { [System.Uri]::EscapeDataString($_[0]) + '=' + [System.Uri]::EscapeDataString($_[1]) }) -join '&'
  $fullPath += '?' + $qs
}

# --- request body: inline text (ASCII safe) or UTF-8 file, BOM stripped ---
$bodyBytes = $null
if ($BodyFile) {
  $bodyBytes = [System.IO.File]::ReadAllBytes((Resolve-Path $BodyFile))
  if ($bodyBytes.Length -ge 3 -and $bodyBytes[0] -eq 239 -and $bodyBytes[1] -eq 187 -and $bodyBytes[2] -eq 191) {
    $newLen = $bodyBytes.Length - 3
    $trimmed = New-Object byte[] $newLen
    if ($newLen -gt 0) { [Array]::Copy($bodyBytes, 3, $trimmed, 0, $newLen) }
    $bodyBytes = $trimmed
  }
} elseif ($Body) {
  $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
}

# --- send: never follow redirects, key only in X-Api-Key header ---
$req = [System.Net.HttpWebRequest]::Create($gateway + $fullPath)
$req.Method = $Method
$req.AllowAutoRedirect = $false
$req.Timeout = $TimeoutSec * 1000
$req.ReadWriteTimeout = $TimeoutSec * 1000
$req.Accept = 'application/json'
$req.Headers.Add('X-Api-Key', $key)
if ($bodyBytes) {
  $req.ContentType = 'application/json'
  $req.ContentLength = $bodyBytes.Length
  $s = $req.GetRequestStream()
  $s.Write($bodyBytes, 0, $bodyBytes.Length)
  $s.Close()
}
try { $resp = $req.GetResponse() }
catch [System.Net.WebException] { $resp = $_.Exception.Response }
if (-not $resp) { Write-Output 'NO_RESPONSE'; exit 1 }
$status = [int]$resp.StatusCode
$reader = New-Object System.IO.StreamReader($resp.GetResponseStream(), [System.Text.Encoding]::UTF8)
$text = $reader.ReadToEnd()
$reader.Close(); $resp.Close()
Write-Output ('HTTP_STATUS:' + $status)
Write-Output $text
if ($status -lt 200 -or $status -ge 300) { exit 1 }
exit 0
