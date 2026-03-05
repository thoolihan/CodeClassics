@echo off

set br=book

xcopy /e /i /y "%br%\boing-master\images" "ch01-boing\images\"
xcopy /e /i /y "%br%\boing-master\music" "ch01-boing\music\"
xcopy /e /i /y "%br%\boing-master\sounds" "ch01-boing\sounds\"

xcopy /e /i /y "%br%\cavern-master\images" "ch02-cavern\images\"
xcopy /e /i /y "%br%\cavern-master\music" "ch02-cavern\music\"
xcopy /e /i /y "%br%\cavern-master\sounds" "ch02-cavern\sounds\"

xcopy /e /i /y "%br%\bunner-master\images" "ch03-bunner\images\"
xcopy /e /i /y "%br%\bunner-master\music" "ch03-bunner\music\"
xcopy /e /i /y "%br%\bunner-master\sounds" "ch03-bunner\sounds\"
