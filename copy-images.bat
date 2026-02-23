@echo off

set br=book

xcopy /e /i /y "%br%\boing-master\images" "ch01-boing\images\"
xcopy /e /i /y "%br%\boing-master\music" "ch01-boing\music\"
xcopy /e /i /y "%br%\boing-master\sounds" "ch01-boing\sounds\"
