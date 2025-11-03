# Start OnlyOffice Document Server with Private IP Support
Write-Host "`n======================================================================"
Write-Host "🚀 Starting OnlyOffice Document Server"
Write-Host "======================================================================`n"

# Stop and remove existing container
Write-Host "1️⃣ Stopping existing container..."
docker stop onlyoffice-documentserver 2>$null
docker rm onlyoffice-documentserver 2>$null

# Start new container with private IP support
Write-Host "2️⃣ Starting new container with private IP support..."
docker run -i -t -d -p 8080:80 `
  -e JWT_ENABLED=false `
  -e WOPI_ENABLED=true `
  -e ALLOW_PRIVATE_IP_ADDRESS=true `
  -e ALLOW_META_IP_ADDRESS=true `
  --name onlyoffice-documentserver `
  onlyoffice/documentserver

Write-Host "`n✅ OnlyOffice Document Server started!"
Write-Host "⏳ Wait 30 seconds for it to fully initialize..."
Write-Host "📡 Access at: http://localhost:8080"
Write-Host "======================================================================`n"
