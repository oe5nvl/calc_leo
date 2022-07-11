# calc_leo

Calculates the position of Low Earth Orbit sattelittes for a given observer location.

# Install
git clone https://github.com/oe5nvl/calc_leo.git

Do not forget to update the TLE-data. Simply delete stations.txt and restart the program

# Start calculation with: 
```
python3 ./leo.py
```
# Prerequisite:
Install skyfiled library (https://rhodesmill.org/skyfield/)
```
pip3 install skyfield
```
# Files:
```
leo.py - main program
spacecrafts.json - list of objects to calculate
config_dss_c.py - config file for paths and URLs - insert oberver location here
```
```
calc_obj.py - class to calculate the leos
```
```
TLE files are automatically downloaded by Skyfield:
stations.txt
amateur.txt
noaa.txt
```
OE5NVL, OE5RNL
