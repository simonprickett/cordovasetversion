#!/usr/bin/pwsh
<#
.SYNOPSIS
  Set version and build numbers for Cordova app for iOS and Android in config.xml
.DESCRIPTION
This scripts is the port of python code to PowerShell to set version and build numbers for Cordova app for iOS and Android in config.xml
.AUTHOR
Frédéric Ntawiniga based on the python scripts by Simon Prickett
#>

Param (
    [ValidateScript({
        $StringArray = $_.Split(".")

        $ErrorFound = $False
        If($StringArray.Length -Lt 3) {
            $ErrorFound = $True
        }
        Else {
            Foreach($String in $StringArray) {
                If( ($String -Match "^\d+$") -Ne $True) {
                    $ErrorFound = $True
                    Break
                }
            }
        }

        If($ErrorFound) {
            Throw "Build Number must be of the form 0.0.0"
        }
        Else {
            $True
        }
    })]
    [String] $VersionNumber = $(Throw "Version Number (-VersionNumber) Required"),
    [ValidateRange(0,[int]::MaxValue)]
    [Int] $BuildNumber = $(Throw "Build Number (-BuildNumber) Required"),
    [ValidateScript({
        If( (Test-Path $_) -Ne $True) {
            Throw "ERROR: $($_) file does not exist"
        }

        $True
    })]
    [String] $ConfigFile = $(Throw "Config File (-ConfigFile) Required")
)

Process {
    [Xml]$XmlTree = Get-Content -Path $ConfigFile

    If($XmlTree.widget -Eq $Null) {
        Throw "Failed to find a single <widget> element in config.xml"
    }
    Else {
        $XmlTree.widget.version = $VersionNumber

        $XmlTree.widget.SetAttribute("android-versionCode", [String]$BuildNumber)
        $XmlTree.widget.SetAttribute("ios-CFBundleVersion", [String]$BuildNumber)

        $XmlTree.Save($ConfigFile)
    }
}
