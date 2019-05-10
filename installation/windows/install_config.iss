; this installation file was written in inno setup

#define MyAppName "Queue Plus"
#define MyAppVersion "v0.3.2 [Alpha]"
#define MyAppPublisher "The Emperium"
#define MyAppURL "https://github.com/the-emperium"

#define UserDirName "your username"

[Setup]
AppId={{D512EDCD-C623-49F3-8605-C44EF4F82CD8}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={userdocs}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=C:\Users\{#UserDirName}\PycharmProjects\queue-plus\LICENSE
PrivilegesRequired=admin
OutputDir=out
OutputBaseFilename=InstallQueuePlus
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "C:\Users\Akiva\PycharmProjects\queue-plus\*"; Excludes: ".idea,__pycache__,\data\*,*.md,*.spec,*.manifest,.gitignore,start.bat"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Run]
Filename: "{app}\installation\windows\postinstall.bat"; WorkingDir: "{app}"; Parameters: """{code:PythonPath}"""; Flags: runascurrentuser runhidden waituntilterminated

[Code]

function CheckPythonVersion(Version: String): Boolean;
var
	PythonFound: Boolean;
begin
	Result := DirExists('C:\Program Files (x86)\Python' + Version + '-32');
end;

function CheckPythonVersionLocal(Version: String): Boolean;
begin
	Result := DirExists(GetEnv('LOCALAPPDATA') + '\Programs\Python\Python' + Version + '-32');
end;

function GetPythonVersion(): String;
var
	PyVersion: String;
begin
	PyVersion := '';

	if CheckPythonVersion('35') or CheckPythonVersionLocal('35') then
		PyVersion := '35';
	if CheckPythonVersion('36') or CheckPythonVersionLocal('36') then
		PyVersion := '36';
	if CheckPythonVersion('37') or CheckPythonVersionLocal('37') then
		PyVersion := '37';
	Result := PyVersion;
end;

{ true: globally installed }
{ false: local installation }
function GetPythonInstallationType(Version: String): Boolean;
begin
	Result := DirExists('C:\Program Files (x86)\Python' + Version + '-32');
end;

function SupportedPythonVersion(): Boolean;
begin
	Result := length(GetPythonVersion()) > 0;
	if Result = False then
		MsgBox('Please install python 3.5 or higher before continuing.', mbCriticalError, 0)
end;

function PythonPath(Param: String): String;
var
	PythonGlobal: Boolean;
begin
	PythonGlobal := GetPythonInstallationType(GetPythonVersion());
	if PythonGlobal = True then
		Result := ExpandConstant('C:\Program Files (x86)\Python' + GetPythonVersion() + '-32')
	else
		Result := ExpandConstant(GetEnv('LOCALAPPDATA') + '\Programs\Python\Python' + GetPythonVersion() + '-32');
end;

function InitializeSetup(): Boolean;
begin
	Result := SupportedPythonVersion();
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  case CurPageID of
      wpFinished : WizardForm.FinishedLabel.Caption := 'Installation Complete! '#13#10'To run Queue Plus just run the start.bat in the installation directory.';
  end;
end;