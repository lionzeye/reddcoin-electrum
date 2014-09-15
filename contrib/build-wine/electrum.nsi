;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "Reddcoin Electrum"
  OutFile "dist/reddcoin-electrum-setup.exe"

  ;Default installation folder
  InstallDir "$PROGRAMFILES\Reddcoin-Electrum"

  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\Reddcoin-Electrum" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel admin

;--------------------------------
;Variables

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Pages

  ;!insertmacro MUI_PAGE_LICENSE "tmp/LICENCE"
  ;!insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY

  ;Start Menu Folder Page Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU"
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Reddcoin-Electrum"
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"

  ;!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder

  !insertmacro MUI_PAGE_INSTFILES

  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section

  SetOutPath "$INSTDIR"

  ;ADD YOUR OWN FILES HERE...
  file /r dist\reddcoin-electrum\*.*

  ;Store installation folder
  WriteRegStr HKCU "Software\Reddcoin-Electrum" "" $INSTDIR

  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"


  CreateShortCut "$DESKTOP\Reddcoin-Electrum.lnk" "$INSTDIR\reddcoin-electrum.exe" ""

  ;create start-menu items
  CreateDirectory "$SMPROGRAMS\Reddcoin-Electrum"
  CreateShortCut "$SMPROGRAMS\Reddcoin-Electrum\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\Reddcoin-Electrum\Reddcoin-Electrum.lnk" "$INSTDIR\reddcoin-electrum.exe" "" "$INSTDIR\reddcoin-electrum.exe" 0

SectionEnd

;--------------------------------
;Descriptions

  ;Assign language strings to sections
  ;!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  ;  !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
  ;!insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...
  RMDir /r "$INSTDIR\*.*"

  RMDir "$INSTDIR"

  Delete "$DESKTOP\Reddcoin-Electrum.lnk"
  Delete "$SMPROGRAMS\Reddcoin-Electrum\*.*"
  RmDir  "$SMPROGRAMS\Reddcoin-Electrum"

  DeleteRegKey /ifempty HKCU "Software\Reddcoin-Electrum"

SectionEnd
