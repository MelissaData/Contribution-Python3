<#
.SYNOPSIS
    Runs the Melissa Contribution Cloud API Python 3 sample.

.DESCRIPTION
    This script runs ContributionPython3.py with python3, passing along the license
    and (if supplied) the contribution fields.

    Overall flow:
      1. Resolve the license (parameter, prompt, or MD_LICENSE environment variable).
      2. Run ContributionPython3.py: with the contribution fields if any was supplied,
         otherwise with only the license (the Python program prompts for each field).

.PARAMETER lat
    Proposed latitude for the address.

.PARAMETER long
    Proposed longitude for the address.

.PARAMETER mak
    Melissa Address Key (MAK) of the address to correct.

.PARAMETER reason
    Reason for the change.

.PARAMETER respondTo
    Contact (e.g. an email address) to respond to about the contribution.

.PARAMETER license
    License string. Resolved in this order:
      1. This parameter.
      2. An interactive prompt, if the parameter was not supplied.
      3. The MD_LICENSE environment variable, if the prompt was left blank.
    Note that the environment variable is the last resort, not the first: running
    without -license always prompts, even when MD_LICENSE is set.

.PARAMETER quiet
    Accepted for parity with other sample scripts; not currently used to suppress output.

.EXAMPLE
    .\ContributionPython3.ps1 -license "your-license"

.EXAMPLE
    .\ContributionPython3.ps1 -lat "33.637562" -long "-117.606887" -mak "8008006245" -reason "GeoPoint Change needed" -respondTo "youremail@melissadata.com" -license "your-license"
#>

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
# No contribution fields supplied -> run with only the license (the program prompts); otherwise pass the supplied ones through.
if ([string]::IsNullOrEmpty($lat) -and [string]::IsNullOrEmpty($long) -and [string]::IsNullOrEmpty($mak) -and [string]::IsNullOrEmpty($reason) -and [string]::IsNullOrEmpty($respondTo)) {
  python3 ContributionPython3.py --license $license 
}
else {
  # Only pass flags that have a value. Windows PowerShell drops empty-string arguments to
  # native programs, which would shift the next flag name into this flag's value.
  # Any field left out here is prompted for by the program.
  $runArgs = @('--license', $license)
  if (-not [string]::IsNullOrEmpty($lat))       { $runArgs += '--lat', $lat }
  if (-not [string]::IsNullOrEmpty($long))      { $runArgs += '--long', $long }
  if (-not [string]::IsNullOrEmpty($mak))       { $runArgs += '--mak', $mak }
  if (-not [string]::IsNullOrEmpty($reason))    { $runArgs += '--reason', $reason }
  if (-not [string]::IsNullOrEmpty($respondTo)) { $runArgs += '--respondTo', $respondTo }
  python3 ContributionPython3.py @runArgs
}
