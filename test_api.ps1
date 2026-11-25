#!/usr/bin/env pwsh

# Test supervisor login
$loginUrl = "http://localhost:5000/api/auth/login"
$loginData = @{
    username = "supervisor1"
    password = "admin123"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

Write-Host "Testing Supervisor Login..."
try {
    $response = Invoke-WebRequest -Uri $loginUrl -Method POST -Body $loginData -Headers $headers -UseBasicParsing
    $loginResult = $response.Content | ConvertFrom-Json
    
    if ($loginResult.access_token) {
        Write-Host "[OK] Login successful!"
        Write-Host "Token: $($loginResult.access_token.Substring(0,20))..."
        
        $token = $loginResult.access_token
        
        # Test dashboard stats endpoint
        $statsUrl = "http://localhost:5000/api/supervisor/dashboard/stats"
        $authHeaders = @{
            "Authorization" = "Bearer $token"
            "Content-Type" = "application/json"
        }
        
        Write-Host "`nTesting /api/supervisor/dashboard/stats..."
        try {
            $statsResponse = Invoke-WebRequest -Uri $statsUrl -Method GET -Headers $authHeaders -UseBasicParsing
            $statsResult = $statsResponse.Content | ConvertFrom-Json
            Write-Host "[OK] Stats Response:"
            Write-Host ($statsResult | ConvertTo-Json -Depth 3)
        } catch {
            Write-Host "[ERROR] Stats endpoint failed: $($_.Exception.Message)"
            $errorResponse = $_.Exception.Response.Content | ConvertFrom-Json
            Write-Host "Error details: $($errorResponse | ConvertTo-Json)"
        }
        
        # Test zones endpoint
        $zonesUrl = "http://localhost:5000/api/supervisor/zones"
        Write-Host "`nTesting /api/supervisor/zones..."
        try {
            $zonesResponse = Invoke-WebRequest -Uri $zonesUrl -Method GET -Headers $authHeaders -UseBasicParsing
            $zonesResult = $zonesResponse.Content | ConvertFrom-Json
            Write-Host "[OK] Zones Response:"
            Write-Host ($zonesResult | ConvertTo-Json -Depth 3)
        } catch {
            Write-Host "[ERROR] Zones endpoint failed: $($_.Exception.Message)"
            $errorResponse = $_.Exception.Response.Content | ConvertFrom-Json
            Write-Host "Error details: $($errorResponse | ConvertTo-Json)"
        }
        
    } else {
        Write-Host "[ERROR] Login failed: No token returned"
        Write-Host $response.Content
    }
} catch {
    Write-Host "[ERROR] $($_.Exception.Message)"
    if ($_.Exception.Response) {
        Write-Host $_.Exception.Response.Content
    }
}
