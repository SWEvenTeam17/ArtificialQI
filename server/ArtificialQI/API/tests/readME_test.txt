
Per avviare i test:

1. Assicurarsi di essere nel percorso/path giusto, ovvero >> C:\Users\Unipd\ProgettoSwe\ArtificialQI\server

2.Poi scrivere >>  .\run-tests.ps1
  per automatizzare l'esecuzione

3. Se da errore ( windows? ) bypassarlo con >> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

4.A questo punto dovrebbe comparire (venv) all'inizio e riprovare a fare .\run-tests.ps1 

5.Ora dovrebbero partire tutti i test all'interno di API/tests