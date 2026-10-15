param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$ArticlePath
)

$ErrorActionPreference = 'Stop'
$resolvedArticle = (Resolve-Path -LiteralPath $ArticlePath).Path
$markdown = Get-Content -LiteralPath $resolvedArticle -Raw -Encoding UTF8
$matches = [regex]::Matches($markdown, '!\[[^\]]*\]\(([^)]+)\)')

if ($matches.Count -eq 0) {
    throw "文章中没有检测到图片：$resolvedArticle"
}

$client = [System.Net.Http.HttpClient]::new()
$failed = $false

try {
    foreach ($match in $matches) {
        $url = $match.Groups[1].Value.Trim()

        if ($url -notmatch '^https://img\.wemd\.app/') {
            $failed = $true
            [PSCustomObject]@{
                Url = $url
                Status = 'INVALID'
                ContentType = ''
                Message = '正式文章必须使用 WeMD 官方图床 URL'
            }
            continue
        }

        try {
            $response = $client.GetAsync($url, [System.Net.Http.HttpCompletionOption]::ResponseHeadersRead).GetAwaiter().GetResult()
            $type = if ($response.Content.Headers.ContentType) { $response.Content.Headers.ContentType.MediaType } else { '' }
            $ok = $response.IsSuccessStatusCode -and $type.StartsWith('image/')
            if (-not $ok) { $failed = $true }

            [PSCustomObject]@{
                Url = $url
                Status = [int]$response.StatusCode
                ContentType = $type
                Message = if ($ok) { 'OK' } else { '图片不可用' }
            }
            $response.Dispose()
        }
        catch {
            $failed = $true
            [PSCustomObject]@{
                Url = $url
                Status = 'ERROR'
                ContentType = ''
                Message = $_.Exception.Message
            }
        }
    }
}
finally {
    $client.Dispose()
}

if ($failed) {
    throw 'WeMD 图片链路检查失败。'
}
