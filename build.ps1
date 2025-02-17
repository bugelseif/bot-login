$exclude = @("venv", "bot-login.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "bot-login.zip" -Force