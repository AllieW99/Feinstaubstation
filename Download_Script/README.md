# Download Script

This is a powershell script to download the CSV data from the sensors 3659 und 3660.<br>
It creates a log of missing data in: [your_path]\CSV\[date]_Download_log.txt

## How to use?

If you want to run the script manually you need to use the following command in a cmd terminal:
```bash
powershell.exe .\Feinstaub_CSV_Downloader.ps1 -Path "[your_path]" -Start_Date "[start_date]"
```

With no parameters it will be created in "C:\Users\[User]\Desktop" and starts with "2015-10-01" as date.
Format of date: "yyyy-MM-dd"