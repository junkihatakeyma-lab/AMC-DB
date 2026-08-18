$files = @(93, 94, 95)
foreach ($n in $files) {
    $jsonPath = "C:\Users\jhatakeyama\.gemini\antigravity\scratch\PartsSearchDB\bom_chunk_${n}.json"
    $outPath = "C:\Users\jhatakeyama\.gemini\antigravity\scratch\PartsSearchDB\parsed_bom_${n}.json"
    
    $json = Get-Content $jsonPath | ConvertFrom-Json
    $out = @()
    foreach ($f in $json) {
        $req = ($f -replace '.*#', '') -replace '\.jpg', ''
        $out += [PSCustomObject]@{
            request_no = $req
            hinmei = "[手書き] "
            components = @()
        }
    }
    $out | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 $outPath
}
