# Download latest Colosseum core / plugin wheels and linter VSIX from GitHub Releases.
# Uses only built-in PowerShell (no gh CLI). Assets land next to this script.

$ErrorActionPreference = 'Stop'

$OutDir = $PSScriptRoot
$Headers = @{
    'User-Agent' = 'colosseum-download-releases'
    'Accept'     = 'application/vnd.github+json'
}

function Get-LatestReleaseAsset {
    param(
        [Parameter(Mandatory)][string]$Repo,
        [Parameter(Mandatory)][string]$Pattern
    )

    $uri = "https://api.github.com/repos/$Repo/releases/latest"
    $release = Invoke-RestMethod -Uri $uri -Headers $Headers
    $asset = $release.assets | Where-Object { $_.name -like $Pattern } | Select-Object -First 1
    if (-not $asset) {
        throw "No asset matching '$Pattern' in $Repo release $($release.tag_name)."
    }

    [pscustomobject]@{
        Repo    = $Repo
        Tag     = $release.tag_name
        Name    = $asset.name
        Url     = $asset.browser_download_url
    }
}

function Save-ReleaseAsset {
    param(
        [Parameter(Mandatory)]$Asset
    )

    $dest = Join-Path $OutDir $Asset.Name
    Write-Host "Downloading $($Asset.Name) from $($Asset.Repo) $($Asset.Tag) ..."
    Invoke-WebRequest -Uri $Asset.Url -Headers $Headers -OutFile $dest
    Write-Host "  -> $dest"
}

$targets = @(
    @{ Repo = 'tps01/colosseum-core';       Pattern = 'colosseum_core-*-py3-none-any.whl' }
    @{ Repo = 'tps01/colosseum-shared';     Pattern = 'colosseum_shared-*-py3-none-any.whl' }
    @{ Repo = 'tps01/colosseum-gui';        Pattern = 'colosseum_gui-*-py3-none-any.whl' }
    @{ Repo = 'tps01/colosseum-host';       Pattern = 'colosseum_host-*-py3-none-any.whl' }
    @{ Repo = 'tps01/colosseum-messaging';  Pattern = 'colosseum_messaging-*-py3-none-any.whl' }
    @{ Repo = 'tps01/colosseum-equipment';  Pattern = 'colosseum_equipment-*-py3-none-any.whl' }
    @{ Repo = 'tps01/colosseum-linter';     Pattern = 'colosseum-linter-*.vsix' }
)

foreach ($t in $targets) {
    $asset = Get-LatestReleaseAsset -Repo $t.Repo -Pattern $t.Pattern
    Save-ReleaseAsset -Asset $asset
}

Write-Host "Done. Downloaded $($targets.Count) assets to $OutDir"
