# HKJC_Result_Scraper

This is a Python-based web scraper, to semi-automatically fetch historical data from the HKJC website.
Currently, a manual change of racecourse code (ST / HV) is needed and the header will be duplicated for each race.

Plans of imporvement:
- Reminder on race missing due to HKJC's server timeout.
- Deal with HKJC Timeout problem - in someday there might be results exist but the server might return timeout or display "No record found". (Added timeout option on v1.1)
- Automatically check both ST & HV on one date.
- Convert Big5 inputstream to UTF-8 format.
- Insert data into the database directly.
- Restructure the whole program, it's a bit messy.
