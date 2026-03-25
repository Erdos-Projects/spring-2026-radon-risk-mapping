@echo off
cd /d C:\Users\john\Desktop\spring-2026-radon-risk-mapping\notebooks\modeling

jupyter nbconvert --to notebook --execute log_regression_pipeline.ipynb --inplace --ExecutePreprocessor.timeout=-1
if errorlevel 1 goto :fail

jupyter nbconvert --to notebook --execute random_forest_pipeline.ipynb --inplace --ExecutePreprocessor.timeout=-1
if errorlevel 1 goto :fail

jupyter nbconvert --to notebook --execute xgboost_pipeline.ipynb --inplace --ExecutePreprocessor.timeout=-1
if errorlevel 1 goto :fail

echo.
echo All three notebook runs completed.
pause
goto :eof

:fail
echo.
echo A notebook run failed. Check the output above.
pause