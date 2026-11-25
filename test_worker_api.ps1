#!/usr/bin/env pwsh

# Test if workers exist and test worker endpoints

$loginUrl = "http://localhost:5000/api/auth/login"
$loginData = @{
    username = "worker1"
    password = "password123"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

Write-Host "Testing Worker Login..."
try {
    $response = Invoke-WebRequest -Uri $loginUrl -Method POST -Body $loginData -Headers $headers -UseBasicParsing
    $loginResult = $response.Content | ConvertFrom-Json
    
    if ($loginResult.access_token) {
        Write-Host "[OK] Worker login successful!"
        
        $token = $loginResult.access_token
        
        # Test worker endpoints
        $workerProfileUrl = "http://localhost:5000/api/worker/profile"
        $authHeaders = @{
            "Authorization" = "Bearer $token"
            "Content-Type" = "application/json"
        }
        
        Write-Host "`nTesting /api/worker/profile..."
        try {
            $profileResponse = Invoke-WebRequest -Uri $workerProfileUrl -Method GET -Headers $authHeaders -UseBasicParsing
            $profileResult = $profileResponse.Content | ConvertFrom-Json
            Write-Host "[OK] Profile Response:"
            Write-Host ($profileResult | ConvertTo-Json -Depth 3)
        } catch {
            Write-Host "[ERROR] Profile endpoint failed"
            Write-Host $_.Exception.Message
        }
    }
} catch {
    Write-Host "[ERROR] Worker login failed: $($_.Exception.Message)"
}
