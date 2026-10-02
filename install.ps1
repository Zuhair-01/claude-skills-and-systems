# install.ps1 — one-command setup for claude-skills-and-systems (Windows)
#   .\install.ps1                 copy everything into Claude Code (~\.claude\skills)
#   .\install.ps1 -Pack frontend  install one pack (see packs\, -ListPacks)
#   .\install.ps1 -Link            use junctions instead of copy (same drive only)
param([string]$Pack = "", [switch]$Link, [switch]$ListPacks, [string]$Target = "")
$Repo = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($ListPacks) { Get-ChildItem "$Repo\packs\*.txt" | ForEach-Object { $_.BaseName }; exit }
if ([string]::IsNullOrEmpty($Target)) { $Target = "$HOME\.claude\skills" }
New-Item -ItemType Directory -Path $Target -Force | Out-Null
if ($Pack -ne "") {
  $pf = "$Repo\packs\$Pack.txt"
  if (!(Test-Path $pf)) { Write-Output "no such pack: $Pack"; exit 1 }
  $Want = Get-Content $pf | Where-Object { $_ -notmatch '^\s*#' -and $_ -notmatch '^\s*$' }
} else {
  $Want = Get-ChildItem -LiteralPath "$Repo\skills" -Directory | Select-Object -ExpandProperty Name
}
$n = 0; $skip = 0
foreach ($s in $Want) {
  if (!(Test-Path "$Repo\skills\$s")) { Write-Output "  skip (not in repo): $s"; $skip++; continue }
  if (!(Test-Path "$Target\$s")) {
    if ($Link) { New-Item -ItemType Junction -Path "$Target\$s" -Target "$Repo\skills\$s" | Out-Null }
    else { Copy-Item -Recurse -Path "$Repo\skills\$s" -Destination "$Target\$s" }
  }
  $n++
}
Write-Output "installed $n skills -> $Target (skipped $skip)"
Write-Output "next: read ROUTING.md to make your agent fire skill-router automatically."
