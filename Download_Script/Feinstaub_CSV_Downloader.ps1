﻿param(
  [parameter(Mandatory=$false)]
  [string]$path = "",
  [string]$Start_Date = (Get-Date -Date "2023-01-01").ToString("yyyy-MM-dd")
)

function Downloader($Path, $Start_Date)
{
    if ($path -eq "")
    {
        $path = Join-Path (Split-Path $PSScriptRoot -Parent) "Python_Script\Resources"
    }
    $today = Get-Date
    $today_string = $today.ToString("yyyy-MM-dd")
    $Datum = Get-Date -Date $Start_Date
    $log_path = Join-Path (Split-Path $PSScriptRoot -Parent) "Python_Script\Resources"
    $File_Counter_3659 = 0
    $File_Counter_3660 = 0

    if ((Test-Path -Path "$($Path)\CSV") -eq $false)
    {
        mkdir "$($Path)\CSV"
    }
    if ((Test-Path -Path "$($Path)\CSV\3659") -eq $false)
    {
        mkdir "$($Path)\CSV\3659"
    }
    if ((Test-Path -Path "$($Path)\CSV\3660") -eq $false)
    {
        mkdir "$($Path)\CSV\3660"
    }
    if ((Test-Path -Path "$($Path)\CSV\$($today_string)_Download_log.txt") -eq $true)
    {
        Clear-Content "$($Path)\CSV\$($today_string)_Download_log.txt"
    }

    while($Datum -le $today)
    {
        $Datum_String = $Datum.ToString("yyyy-MM-dd")
        $Path_3659 = $Path + "\CSV\3659\" + "$($Datum_String)_sds011_sensor_3659.csv"
        $Path_3660 = $Path + "\CSV\3660\" + "$($Datum_String)_dht22_sensor_3660.csv"

        if ($Datum.Year -eq (Get-Date).Year)
        {
            $URL_3659 = "https://archive.sensor.community/$($Datum_String)/$($Datum_String)_sds011_sensor_3659.csv"
            $URL_3660 = "https://archive.sensor.community/$($Datum_String)/$($Datum_String)_dht22_sensor_3660.csv"
        }
        else
        {
            $URL_3659 = "https://archive.sensor.community/$($Datum_String.Substring(0, 4))/$($Datum_String)/$($Datum_String)_sds011_sensor_3659.csv"
            $URL_3660 = "https://archive.sensor.community/$($Datum_String.Substring(0, 4))/$($Datum_String)/$($Datum_String)_dht22_sensor_3660.csv"
        }
        
        try
        {
            if((Test-Path -Path $Path_3659) -ne $true)
            {
                Invoke-WebRequest -Uri $URL_3659 -OutFile $Path_3659 -UseBasicParsing
                $File_Counter_3659 += 1
            }
        }
        catch
        {
            Write-Output "$($Datum_String)_sds011_sensor_3659.csv not found" >> "$($log_path)\$($today_string)_Download_log.txt"
        }

        try
        {
            if((Test-Path -Path $Path_3660) -ne $true)
            {
                Invoke-WebRequest -Uri $URL_3660 -OutFile $Path_3660 -UseBasicParsing
                $File_Counter_3660 += 1
            }
        }
        catch
        {
            Write-Output "$($Datum_String)_dht22_sensor_3660.csv not found" >> "$($log_path)\$($today_string)_Download_log.txt"
        }

        $Datum = $Datum.AddDays(1)
    }
    Write-Output "$($File_Counter_3659) Files Downloaded for Sensor 3659"
    Write-Output "$($File_Counter_3660) Files Downloaded for Sensor 3660"
}

Downloader -Path $Path -Start_Date $Start_Date