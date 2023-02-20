function Downloader($Path, $Start_Date)
{
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

    $today = Get-Date
    $Datum = Get-Date -Date $Start_Date
    while($Datum -le $today)
    {
        $Datum_String = $Datum.ToString("yyyy-MM-dd")
        $Path_3659 = $Path + "\CSV\3659\" + "$($Datum_String)_sds011_sensor_3659.csv"
        $Path_3660 = $Path + "\CSV\3660\" + "$($Datum_String)_dht22_sensor_3660.csv"
        $URL_3659 = "http://archive.sensor.community/$($Datum_String)/$($Datum_String)_sds011_sensor_3659.csv"
        $URL_3660 = "http://archive.sensor.community/$($Datum_String)/$($Datum_String)_dht22_sensor_3660.csv"
        $Status_3659 = invoke-webrequest -Uri $URL_3659 -UseBasicParsing
        $Status_3660 = invoke-webrequest -Uri $URL_3660 -UseBasicParsing

        if(($Status_3659.StatusCode -eq 200) -and ((Test-Path -Path $Path_3659) -ne $true))
        {
            Invoke-WebRequest -Uri $URL_3659 -OutFile $Path_3659 -UseBasicParsing
        }
        if(($Status_3660.StatusCode -eq 200) -and ((Test-Path -Path $Path_3660) -ne $true))
        {
            Invoke-WebRequest -Uri $URL_3660 -OutFile $Path_3660 -UseBasicParsing
        }

        $Datum = $Datum.AddDays(1)
    }
}

Downloader -Path "C:\Users\rouven.imhoff\Desktop" -Start_Date "2023-01-18"