# Name:    ContributionCloudAPI
# Purpose: Execute the ContributionCloudAPI program

######################### Parameters ##########################
param(
    $lat = '', 
    $long = '',
    $mak = '',
    $reason = '',
    $respondTo = '',
    $license = '', 
    [switch]$quiet = $false
    )

########################## Main ############################
Write-Host "`n======================== Melissa Contribution Cloud API ========================`n"

# Get license (either from parameters or user input)
if ([string]::IsNullOrEmpty($license) ) {
  $license = Read-Host "Please enter your license string"
}

# Check for License from Environment Variables 
if ([string]::IsNullOrEmpty($license) ) {
  $license = $env:MD_LICENSE 
}

if ([string]::IsNullOrEmpty($license)) {
  Write-Host "`nLicense String is invalid!"
  Exit
}

# Run project
if ([string]::IsNullOrEmpty($lat) -and [string]::IsNullOrEmpty($long) -and [string]::IsNullOrEmpty($mak) -and [string]::IsNullOrEmpty($reason) -and [string]::IsNullOrEmpty($respondTo)) {
  python3 ContributionPython3.py --license $license 
}
else {
  python3 ContributionPython3.py --license $license --lat $lat --long $long --mak $mak --reason $reason --respondTo $respondTo
}
