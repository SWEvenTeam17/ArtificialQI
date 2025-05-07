# server/run-tests.ps1

# Attiva l'ambiente virtuale
& ".\venv\Scripts\Activate.ps1"

# Carica le variabili da .env
Get-Content .env | ForEach-Object {
    $name, $value = $_ -split '=', 2
    [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), "Process")
}

# Esegui i test con output dettagliato e copertura
pytest -v --cov=ArtificialQI/API ArtificialQI/API/tests/
