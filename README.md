# HKJC_Result_Scraper

This is a Python-based web scraper, to semi-automatically fetch historically data from HKJC website.
Currently, manual change of racecourse code (ST / HV) is needed and header will be duplicated for each race.

Plans of imporvement:
- Reminder on race missing due to HKJC's server timeout.
- Deal with HKJC Timeout problem - some days may have result but HKJC server would timeout and displaying "No record found".
- Automatically check both ST & HV in one date.
- Convert Big5 inputstream to UTF-8 format.
- Insert data to database directly.
- Restructure the whole program, it's a bit messy.
