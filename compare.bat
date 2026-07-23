@echo off
setlocal enabledelayedexpansion

:: Check if both files were provided
if "%~2"=="" (
    echo Usage: %~nx0 ^<file1^> ^<file2^>
    exit /b 1
)

set "file1=%~1"
set "file2=%~2"

:: Fetch changed line strings for both files
call :GetChangedLines "!file1!" changes1
call :GetChangedLines "!file2!" changes2

:: Handle cases where no changes exist
if "!changes1!"=="" set "changes1=None"
if "!changes2!"=="" set "changes2=None"

:: Compare the results and output
if "!changes1!"=="!changes2!" (
    echo Both files have the same changes.
    echo Changes are at line: !changes1!
) else (
    echo The files have changes on different lines.
    echo Changes in !file1! are at line: !changes1!
    echo Changes in !file2! are at line: !changes2!
)

exit /b 0

:: ---------------------------------------------------------
:: Function: GetChangedLines
:: Parses `git diff` to extract modified line numbers
:: ---------------------------------------------------------
:GetChangedLines
set "target_file=%~1"
set "result="

:: git diff -U0 shows zero context lines, making it easy to grab just the @@ headers
for /f "usebackq tokens=3" %%A in (`git diff -U0 "!target_file!" 2^>nul ^| findstr "^@@"`) do (
    set "chunk=%%A"
    
    :: Remove the '+' sign from the header
    set "chunk=!chunk:+=!"
    
    :: Parse the starting line and the count of modified lines
    for /f "tokens=1,2 delims=," %%B in ("!chunk!") do (
        set "start=%%B"
        set "count=%%C"
        
        :: If there is no comma, only 1 line was changed
        if "!count!"=="" set "count=1"
        
        :: Format the string based on the number of lines modified
        if "!count!"=="0" (
            set "line_str=!start!"
        ) else if "!count!"=="1" (
            set "line_str=!start!"
        ) else (
            set /a "end=start + count - 1"
            set "line_str=!start!->!end!"
        )
        
        :: Append to the result variable
        if "!result!"=="" (
            set "result=!line_str!"
        ) else (
            set "result=!result!, !line_str!"
        )
    )
)

:: Pass the result back to the variable name provided in %2
set "%~2=!result!"
exit /b 0