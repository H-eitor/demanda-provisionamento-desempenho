$concurrency_levels = @(10, 50, 100, 200)
$endpoints = @(
    @{ name="cpu"; url="http://localhost:8080/cpu?n=3000000" },
    @{ name="memory"; url="http://localhost:8080/memory?size=1500" },
    @{ name="io"; url="http://localhost:8080/io?size=20" }
)

$cenario = Read-Host "Digite o nome do cenario atual (ex: 2c1g)"
$logfile = "resultado_$cenario.txt"

foreach ($ep in $endpoints) {
    foreach ($c in $concurrency_levels) {
        Write-Host "Testando $($ep.name) com -c $c..."
        Add-Content -Path $logfile -Value "`n=== Teste: $($ep.name) | Concorrencia: $c ==="
        # Executa o ab e joga a saída para o arquivo
        .\ab.exe -n 1000 -c $c $($ep.url) | Out-File -Append -FilePath $logfile
        Start-Sleep -Seconds 2 # Pausa para a VM respirar entre os testes
    }
}
Write-Host "Bateria finalizada! Resultados salvos em $logfile"