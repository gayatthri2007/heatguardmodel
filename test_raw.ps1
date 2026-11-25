#!/usr/bin/env pwsh

# Test with raw error output
$loginUrl = "http://localhost:5000/api/auth/login"
$loginData = @{
    username = "worker1"
    password = "password123"
} | ConvertTo-Json

Write-Host "Logging in..."
$response = Invoke-WebRequest -Uri $loginUrl -Method POST -Body $loginData -Headers @{"Content-Type" = "application/json"} -UseBasicParsing
$loginResult = $response.Content | ConvertFrom-Json
$token = $loginResult.access_token

Write-Host "Token: $($token.Substring(0, 30))..."

# Try the worker profile endpoint without error handling first
$profileUrl = "http://localhost:5000/api/worker/profile"
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

Write-Host "Fetching worker profile..."
$response = Invoke-WebRequest -Uri $profileUrl -Method GET -Headers $headers -UseBasicParsing -ErrorAction Stop
Write-Host "Status Code: $($response.StatusCode)"
Write-Host "Response:`n$($response.Content)"
