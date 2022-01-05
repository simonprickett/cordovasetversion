#!/usr/bin/pwsh
<#
.SYNOPSIS
  Set version and build numbers for Cordova app for iOS and Android in config.xml

.DESCRIPTION
This scripts is the port of python code to PowerShell to set version and build numbers for Cordova app for iOS and Android in config.xml

.AUTHOR
Frédéric Ntawiniga based on the python scripts by Simon Prickett
#>
Function Set-CordovaVersion {
  [CmdletBinding()]
  Param (
    [parameter(Mandatory)]
        [ValidateScript({
            
        })]
        [String] $VersionNumber,
    [parameter(Mandatory)]
    [Int] $BuildNumber,
    [parameter(Mandatory)]
        [ValidateScript({
            
        })]
    [String] $ConfigFile
  )

  Process {
  }
