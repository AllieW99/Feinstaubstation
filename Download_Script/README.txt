Script zum Downloaden von den CSV Dateien der Senosren 3659 und 3660.
Schreibt log der Fehlenden Dateien in: [Dein_Speicher_Pfad]\CSV\[Datum_der_datei]_Download_log.txt

###
cmd Aufruf: powershell.exe .\Feinstaub_CSV_Downloader.ps1 -Path "[Dein_Speicher_Pfad]" -Start_Date "[Datum_der_ersten_gewünschten_Datei]"
###

Wenn keine Parameter mit angegeben werden nimmt das Script "C:\Useres\[User]\Desktop" als Pfad und "2015-10-01" als Start Datum.
Das Datum muss in diesem Format angegeben werden: "yyyy-MM-dd"