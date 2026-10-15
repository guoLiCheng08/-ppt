[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$Text,

    [ValidateRange(-10, 10)]
    [int]$Rate = 0,

    [ValidateRange(0, 100)]
    [int]$Volume = 100
)

$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Speech

$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $speaker.Rate = $Rate
    $speaker.Volume = $Volume

    # 优先使用中文语音；没有中文语音时回退到系统默认语音。
    $zhVoice = $speaker.GetInstalledVoices() |
        Where-Object { $_.VoiceInfo.Culture.Name -in @('zh-CN', 'zh-Hans', 'zh') } |
        Select-Object -First 1

    if ($null -ne $zhVoice) {
        $speaker.SelectVoice($zhVoice.VoiceInfo.Name)
    }

    $speaker.Speak($Text)
}
finally {
    $speaker.Dispose()
}
