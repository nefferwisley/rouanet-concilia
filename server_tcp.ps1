$port = 8080
$folderPath = "C:\Users\kATE\.gemini\antigravity\scratch\rouanet-ux-demo"
$ip = [System.Net.IPAddress]::Any
$listener = New-Object System.Net.Sockets.TcpListener($ip, $port)

try {
    $listener.Start()
    Write-Host "Servidor Web TCP Ativo na porta $port..."
} catch {
    Write-Host "Erro ao iniciar porta: $_"
    exit 1
}

while ($true) {
    try {
        $client = $listener.AcceptTcpClient()
        $stream = $client.GetStream()
        $reader = New-Object System.IO.StreamReader($stream)
        
        $requestLine = $reader.ReadLine()
        if ($requestLine) {
            $tokens = $requestLine.Split(" ")
            if ($tokens.Length -ge 2) {
                $url = $tokens[1]
                $localPath = $url.Split("?")[0]
                if ($localPath -eq "/" -or $localPath -eq "") {
                    $localPath = "/index.html"
                }
                
                $filePath = Join-Path $folderPath $localPath.TrimStart('/')
                
                if (Test-Path $filePath -PathType Leaf) {
                    $bytes = [System.IO.File]::ReadAllBytes($filePath)
                    $contentType = "text/html; charset=utf-8"
                    if ($filePath.EndsWith(".css")) { $contentType = "text/css" }
                    elseif ($filePath.EndsWith(".js")) { $contentType = "application/javascript" }
                    elseif ($filePath.EndsWith(".json")) { $contentType = "application/json" }
                    elseif ($filePath.EndsWith(".md")) { $contentType = "text/markdown; charset=utf-8" }
                    
                    $header = "HTTP/1.1 200 OK`r`nContent-Type: $contentType`r`nContent-Length: $($bytes.Length)`r`nAccess-Control-Allow-Origin: *`r`nConnection: close`r`n`r`n"
                    $headerBytes = [System.Text.Encoding]::UTF8.GetBytes($header)
                    $stream.Write($headerBytes, 0, $headerBytes.Length)
                    $stream.Write($bytes, 0, $bytes.Length)
                } else {
                    $notFound = "HTTP/1.1 404 Not Found`r`nContent-Length: 13`r`nConnection: close`r`n`r`n404 Not Found"
                    $notFoundBytes = [System.Text.Encoding]::UTF8.GetBytes($notFound)
                    $stream.Write($notFoundBytes, 0, $notFoundBytes.Length)
                }
            }
        }
        $stream.Close()
        $client.Close()
    } catch {
        # Continua escutando conexões
    }
}
