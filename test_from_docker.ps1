# Test if OnlyOffice container can reach Flask
Write-Host "`n======================================================================"
Write-Host "🧪 Testing OnlyOffice → Flask Connection"
Write-Host "======================================================================`n"

Write-Host "1️⃣ Testing from OnlyOffice container..."
docker exec onlyoffice-documentserver curl -v http://host.docker.internal:5000/api/health

Write-Host "`n2️⃣ Testing with IP address..."
docker exec onlyoffice-documentserver curl -v http://192.168.0.104:5000/api/health

Write-Host "`n======================================================================"
Write-Host "If both tests show 'status: ok', OnlyOffice can reach Flask!"
Write-Host "======================================================================`n"
