param([switch]$Execute, [string]$ReportName = 'cleanup.json')
$ErrorActionPreference = 'Stop'
if ($ReportName -notmatch '^[A-Za-z0-9_.-]+\.json$') { throw 'ReportName must be a JSON filename without a directory.' }
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$taskPrefix = $taskRoot.TrimEnd('\') + '\'
$directories = @('image_tex/build', 'image_tex/backups', 'image_tex/unused', '_minted-main', 'scripts/__pycache__', 'scripts/.mypy_cache', 'tmp/minted-review', 'tmp/a1-review', 'tmp/figure-layout', 'tmp/figure-size-review', 'tmp/backmatter')
$directories += @(Get-ChildItem -LiteralPath $taskRoot -Directory -Force | Where-Object { $_.Name -like '_minted-*' -and $_.Name -ne '_minted-main' } | ForEach-Object Name)
$files = @('image_tex/current_work.md', 'image_tex/continuous_notes.md', 'main.aux', 'main.log', 'main.out', 'main.toc', 'main.synctex.gz', 'main.idx', 'main.ind', 'main.ilg', 'main.fdb_latexmk', 'main.fls', 'main.xdv')
$targets = @()
foreach ($relative in ($directories + $files)) {
    $absolute = [IO.Path]::GetFullPath((Join-Path $taskRoot $relative))
    if (-not $absolute.StartsWith($taskPrefix, [StringComparison]::OrdinalIgnoreCase)) { throw "Outside workspace: $absolute" }
    if (Test-Path -LiteralPath $absolute) {
        $item = Get-Item -LiteralPath $absolute -Force
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Linked target: $absolute" }
        $contents = if ($item.PSIsContainer) { @(Get-ChildItem -LiteralPath $absolute -File -Recurse -Force) } else { @($item) }
        $targets += [pscustomobject]@{path=$relative; absolute=$absolute; directory=$item.PSIsContainer; files=$contents.Count; bytes=($contents | Measure-Object Length -Sum).Sum}
    }
}
if (-not $Execute) { $targets | Select-Object path,files,bytes; return }

# Hash formal sources, scripts, original artwork, and the published PDF before cleanup.
$protected = @(Get-Item -LiteralPath (Join-Path $taskRoot 'main.tex'), (Join-Path $taskRoot 'main.pdf'), (Join-Path $taskRoot 'image_tex/common.tex'), (Join-Path $taskRoot 'image_tex/manifest.json'), (Join-Path $taskRoot 'image_tex/validation.json'))
foreach ($folder in (@('chapter','cover','colophon','introduction','preface','images','backmatter') + (1..13 | ForEach-Object { 'image_tex/ch{0:d2}' -f $_ }))) {
    $protected += @(Get-ChildItem -LiteralPath (Join-Path $taskRoot $folder) -File -Recurse -Force)
}
$protected += @(Get-ChildItem -LiteralPath $PSScriptRoot -File -Force)
$protected += @(Get-ChildItem -LiteralPath (Join-Path $taskRoot 'image_tex') -File -Filter '*.tex')
$protected += @(Get-Item -LiteralPath (Join-Path $taskRoot '.latexmkrc'), (Join-Path $taskRoot 'make.bat'), (Join-Path $taskRoot 'Makefile'), (Join-Path $taskRoot 'README.md'), (Join-Path $taskRoot 'image_tex/progress.json'))
$before = @{}
foreach ($item in $protected) { $before[$item.FullName] = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash }

$archive = Join-Path $taskRoot 'image_tex/reports'
New-Item -ItemType Directory -Path $archive -Force | Out-Null
$archived = @()
foreach ($name in @('final-book-validation.json','final-native-audit.json','final-pdf-audit.json','final-native-book-batch.json','final-native-book-freeze.json','final-native-book-published.json','book-check-result.json','final-scan.txt')) {
    $source = Join-Path $taskRoot "image_tex/build/$name"
    $destination = Join-Path $archive $name
    if (Test-Path -LiteralPath $source) {
        Copy-Item -LiteralPath $source -Destination $destination -Force
        if ((Get-FileHash -LiteralPath $source).Hash -ne (Get-FileHash -LiteralPath $destination).Hash) { throw "Archive mismatch: $name" }
        $archived += $name
    } elseif (-not (Test-Path -LiteralPath $destination)) { throw "Missing final report: $name" }
}

foreach ($target in $targets) {
    # Recheck every resolved absolute path immediately before recursive deletion.
    $checked = [IO.Path]::GetFullPath($target.absolute)
    if (-not $checked.StartsWith($taskPrefix, [StringComparison]::OrdinalIgnoreCase)) { throw "Outside workspace: $checked" }
    if ($target.directory) { Remove-Item -LiteralPath $checked -Recurse -Force } else { Remove-Item -LiteralPath $checked -Force }
}
foreach ($entry in $before.GetEnumerator()) {
    if ((Get-FileHash -LiteralPath $entry.Key -Algorithm SHA256).Hash -ne $entry.Value) { throw "Protected file changed: $($entry.Key)" }
}
$report = [ordered]@{
    status='complete'; date=(Get-Date -Format 'yyyy-MM-dd'); archived_reports=$archived
    removed=@($targets | Select-Object path,files,bytes)
    removed_bytes=($targets | Measure-Object bytes -Sum).Sum
    protected_files_verified=$before.Count
    protected_files_unchanged=$true
    published_pdf_sha256=(Get-FileHash -LiteralPath (Join-Path $taskRoot 'main.pdf')).Hash.ToLowerInvariant()
    note='Historical manifest evidence paths refer to removed previews and frozen builds. Regenerate evidence before running those validation workflows.'
}
$report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $archive $ReportName) -Encoding utf8
[pscustomobject]$report | Select-Object status,removed_bytes,protected_files_verified,published_pdf_sha256 | ConvertTo-Json
