# Test OnlyOffice callback endpoint from Docker container
Write-Host "`n======================================================================"
Write-Host "🧪 Testing OnlyOffice Callback Endpoint"
Write-Host "======================================================================`n"

Write-Host "1️⃣ Testing callback from OnlyOffice container..."
docker exec onlyoffice-documentserver curl -v -X POST `
  -H "Content-Type: application/json" `
  -d '{\"status\":1}' `
  http://192.168.0.104:5000/api/onlyoffice/callback/test.docx

Write-Host "`n======================================================================"
Write-Host "If you see 'error: 0', the callback endpoint is working!"
Write-Host "======================================================================`n"
