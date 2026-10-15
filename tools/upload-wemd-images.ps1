param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string[]]$Path,

    [string]$ServerUrl = 'https://api.wemd.app/upload',

    [ValidateRange(1, 5)]
    [int]$MaxAttempts = 3
)

$ErrorActionPreference = 'Stop'

function Send-WeMDImage {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ImagePath
    )

    $resolved = (Resolve-Path -LiteralPath $ImagePath).Path
    $item = Get-Item -LiteralPath $resolved

    if ($item.Length -gt 10MB) {
        throw "图片超过 WeMD 10MB 上传上限：$resolved"
    }

    for ($attempt = 1; $attempt -le $MaxAttempts; $attempt += 1) {
        $client = [System.Net.Http.HttpClient]::new()
        $client.Timeout = [TimeSpan]::FromSeconds(90)
        $form = [System.Net.Http.MultipartFormDataContent]::new()
        $stream = [System.IO.File]::OpenRead($resolved)
        $content = [System.Net.Http.StreamContent]::new($stream)
        $content.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse('image/png')
        $disposition = [System.Net.Http.Headers.ContentDispositionHeaderValue]::new('form-data')
        $disposition.Name = '"file"'
        $disposition.FileName = '"' + $item.Name + '"'
        $content.Headers.ContentDisposition = $disposition
        $form.Add($content)

        try {
            $response = $client.PostAsync($ServerUrl, $form).GetAwaiter().GetResult()
            $body = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()

            if (-not $response.IsSuccessStatusCode) {
                throw "上传失败，HTTP $([int]$response.StatusCode)：$body"
            }

            $json = $body | ConvertFrom-Json
            if (-not $json.url) {
                throw "上传接口未返回图片地址：$body"
            }

            return [PSCustomObject]@{
                Path = $resolved
                Url = [string]$json.url
                Status = 'Uploaded'
                Attempt = $attempt
            }
        }
        catch {
            if ($attempt -eq $MaxAttempts) {
                throw
            }
        }
        finally {
            $form.Dispose()
            $stream.Dispose()
            $client.Dispose()
        }
    }
}

foreach ($imagePath in $Path) {
    Send-WeMDImage -ImagePath $imagePath
}
