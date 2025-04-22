
Per avviare i test:

1. Assicurarsi di essere nel percorso/path giusto, ovvero >> C:\Users\Unipd\ProgettoSwe\ArtificialQI\server

2.Poi attivare l'ambiente virtuale con >>  .\venv\Scripts\activate 

3. Se da errore ( windows? ) bypassarlo con >> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

4.A questo punto dovrebbe comparire (venv) all'inizio, scrivere sul terminale >> cd ArtificialQI
  in modo da avere un nuovo path >> C:\Users\Unipd\ProgettoSwe\ArtificialQI\server\ArtificialQI 

5. Ora installare le varie dipendende in requirements.txt con >>  pip install -r requirements.txt

6.Una volta installato tutto, eseguire i test con >> python manage.py test API.tests
 e dovrebbero partire i test.

7. Alla fine dovrebbe comparire il tempo della Run, il numero di errori e la distruzione del database, così >> 
   \ Ran 6 tests in 0.017s

   \ FAILED (errors=4)
   \ Destroying test database for alias 'default'...