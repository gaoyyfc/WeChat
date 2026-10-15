param(
    [Parameter(Mandatory = $true)]
    [string]$FinalDirectory
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$sourceDirectory = Join-Path $FinalDirectory 'source'
$coverSource = Join-Path $sourceDirectory 'cover-source.png'
$readingSource = Join-Path $sourceDirectory 'image-01-source.png'
$cardSource = Join-Path $sourceDirectory 'image-02-base.png'
$coverOutput = Join-Path $FinalDirectory 'cover.png'
$readingOutput = Join-Path $FinalDirectory 'image-01.png'
$cardOutput = Join-Path $FinalDirectory 'image-02.png'
$previewOutput = Join-Path $FinalDirectory 'preview-contact-sheet.png'

function New-CroppedBitmap {
    param(
        [Parameter(Mandatory = $true)] [System.Drawing.Image]$Source,
        [Parameter(Mandatory = $true)] [int]$Width,
        [Parameter(Mandatory = $true)] [int]$Height
    )

    $targetRatio = $Width / $Height
    $sourceRatio = $Source.Width / $Source.Height
    if ($sourceRatio -gt $targetRatio) {
        $cropHeight = $Source.Height
        $cropWidth = [int][Math]::Round($cropHeight * $targetRatio)
        $cropX = [int][Math]::Round(($Source.Width - $cropWidth) / 2)
        $cropY = 0
    }
    else {
        $cropWidth = $Source.Width
        $cropHeight = [int][Math]::Round($cropWidth / $targetRatio)
        $cropX = 0
        $cropY = [int][Math]::Round(($Source.Height - $cropHeight) / 2)
    }

    $bitmap = [System.Drawing.Bitmap]::new($Width, $Height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
        $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $destination = [System.Drawing.Rectangle]::new(0, 0, $Width, $Height)
        $sourceRect = [System.Drawing.Rectangle]::new($cropX, $cropY, $cropWidth, $cropHeight)
        $graphics.DrawImage($Source, $destination, $sourceRect, [System.Drawing.GraphicsUnit]::Pixel)
    }
    finally {
        $graphics.Dispose()
    }
    return $bitmap
}

function Save-CroppedImage {
    param(
        [Parameter(Mandatory = $true)] [string]$InputPath,
        [Parameter(Mandatory = $true)] [string]$OutputPath,
        [Parameter(Mandatory = $true)] [int]$Width,
        [Parameter(Mandatory = $true)] [int]$Height
    )

    $source = [System.Drawing.Image]::FromFile($InputPath)
    try {
        $result = New-CroppedBitmap -Source $source -Width $Width -Height $Height
        try {
            $result.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
        }
        finally {
            $result.Dispose()
        }
    }
    finally {
        $source.Dispose()
    }
}

Save-CroppedImage -InputPath $coverSource -OutputPath $coverOutput -Width 1880 -Height 800
Save-CroppedImage -InputPath $readingSource -OutputPath $readingOutput -Width 1600 -Height 1200

$cardBase = [System.Drawing.Image]::FromFile($cardSource)
try {
    $card = New-CroppedBitmap -Source $cardBase -Width 1200 -Height 1600
}
finally {
    $cardBase.Dispose()
}

$graphics = [System.Drawing.Graphics]::FromImage($card)
$fontFamily = [System.Drawing.FontFamily]::new('Microsoft YaHei UI')
$deep = [System.Drawing.ColorTranslator]::FromHtml('#39352F')
$brown = [System.Drawing.ColorTranslator]::FromHtml('#AC735C')
$green = [System.Drawing.ColorTranslator]::FromHtml('#829480')
$deepBrush = [System.Drawing.SolidBrush]::new($deep)
$brownBrush = [System.Drawing.SolidBrush]::new($brown)
$greenBrush = [System.Drawing.SolidBrush]::new($green)
$titleFont = [System.Drawing.Font]::new($fontFamily, 54, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$numberFont = [System.Drawing.Font]::new($fontFamily, 34, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$headingFont = [System.Drawing.Font]::new($fontFamily, 44, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$placeFont = [System.Drawing.Font]::new($fontFamily, 38, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
$adviceFont = [System.Drawing.Font]::new($fontFamily, 34, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
$footerFont = [System.Drawing.Font]::new($fontFamily, 30, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)

try {
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias

    $graphics.DrawString('给自己留半天', $titleFont, $deepBrush, 76, 70)

    $graphics.DrawString('01', $numberFont, $brownBrush, 82, 312)
    $graphics.DrawString('想安静', $headingFont, $deepBrush, 150, 302)
    $graphics.DrawString('图书馆或书店', $placeFont, $deepBrush, 82, 372)
    $graphics.DrawString('找一个能坐下、无需赶路的地方', $adviceFont, $deepBrush, 82, 438)

    $graphics.DrawString('02', $numberFont, $greenBrush, 82, 692)
    $graphics.DrawString('想走走', $headingFont, $deepBrush, 150, 682)
    $graphics.DrawString('公园或绿道', $placeFont, $deepBrush, 82, 752)
    $graphics.DrawString('定好简单的起点和终点', $adviceFont, $deepBrush, 82, 818)

    $graphics.DrawString('03', $numberFont, $brownBrush, 82, 1062)
    $graphics.DrawString('想体验', $headingFont, $deepBrush, 150, 1052)
    $graphics.DrawString('展览、手作或公共文化活动', $placeFont, $deepBrush, 82, 1122)
    $graphics.DrawString('先查开放时间、预约和费用', $adviceFont, $deepBrush, 82, 1188)

    $footerFormat = [System.Drawing.StringFormat]::new()
    $footerFormat.Alignment = [System.Drawing.StringAlignment]::Center
    $footerRect = [System.Drawing.RectangleF]::new(90, 1450, 1020, 60)
    $graphics.DrawString('只选一个主要目的地，把时间留给自己。', $footerFont, $deepBrush, $footerRect, $footerFormat)
    $footerFormat.Dispose()

    $card.Save($cardOutput, [System.Drawing.Imaging.ImageFormat]::Png)
}
finally {
    $graphics.Dispose()
    $titleFont.Dispose()
    $numberFont.Dispose()
    $headingFont.Dispose()
    $placeFont.Dispose()
    $adviceFont.Dispose()
    $footerFont.Dispose()
    $fontFamily.Dispose()
    $deepBrush.Dispose()
    $brownBrush.Dispose()
    $greenBrush.Dispose()
    $card.Dispose()
}

$cover = [System.Drawing.Image]::FromFile($coverOutput)
$reading = [System.Drawing.Image]::FromFile($readingOutput)
$method = [System.Drawing.Image]::FromFile($cardOutput)
$preview = [System.Drawing.Bitmap]::new(1800, 2160, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$previewGraphics = [System.Drawing.Graphics]::FromImage($preview)
try {
    $previewGraphics.Clear([System.Drawing.Color]::FromArgb(248, 243, 235))
    $previewGraphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $previewGraphics.DrawImage($cover, [System.Drawing.Rectangle]::new(60, 60, 1680, 715))
    $previewGraphics.DrawImage($reading, [System.Drawing.Rectangle]::new(60, 835, 1050, 788))
    $previewGraphics.DrawImage($method, [System.Drawing.Rectangle]::new(1160, 835, 570, 760))

    $labelFont = [System.Drawing.Font]::new('Microsoft YaHei UI', 28, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $labelBrush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#39352F'))
    try {
        $previewGraphics.DrawString('封面图  2.35:1', $labelFont, $labelBrush, 60, 790)
        $previewGraphics.DrawString('正文图1  4:3', $labelFont, $labelBrush, 60, 1650)
        $previewGraphics.DrawString('正文图2  3:4', $labelFont, $labelBrush, 1160, 1650)
    }
    finally {
        $labelFont.Dispose()
        $labelBrush.Dispose()
    }

    $preview.Save($previewOutput, [System.Drawing.Imaging.ImageFormat]::Png)
}
finally {
    $previewGraphics.Dispose()
    $preview.Dispose()
    $cover.Dispose()
    $reading.Dispose()
    $method.Dispose()
}

Get-Item -LiteralPath $coverOutput, $readingOutput, $cardOutput, $previewOutput |
    Select-Object FullName, Length
