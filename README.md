## Test System
#### This tool is based on wxpython to build the GUI testing system_
- _module_ :  plug-in function.
- _project_ : All Project can use to test.
- _source_ :  The element of the program to build the framework. 
- _ui_ : All UI panel of the test program.
- main.py

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)
## Installation
#### This test system requires  [python](https://www.python.org/downloads/)  v3.7+ to run
##### Install the dependencies and start the program
#
```sh
pip install pandas
pip install wxpython
pip install pypubsub
pip install ObjectListView
python main.py
```
##### General  site-package
#
```sh
pip install numpy
pip install pandas
pip install matplotlib
```
##### Optional install site-package
Use the `generate_report_csv` function on the  _./module/generate_report_csv.py_ 
```sh
pip install csv
```
Use the `login` function on the  _./module/login_ 
```sh
pip install zeep
pip install request
```
Use to control instrument
```sh
pip install pyaardvark
pip install pyvisa
pip install pyserial
pip install opencv-python
```
Use to remote SSH connection
```sh
pip install paramiko
```
Use to math computation
```sh
pip install scipy
```


## How to create new project
##### Create new project need to include:
- config : JSON setting file, Specification.csv 
- src : The element use on the test flow, eg. button, image, icon.
- func: The common function use on the test flow.
- task: All task 

> Note: `Specification.csv ` is used to control the test process, and data display
> Note: `func` folder must have initial.py as the first step of test process, while, others files can be modify without any problem.

##### Specification.csv
The test process will fetch `script`, `function` and `parameter` to execute
- `script`: based on the task file name to assign
- `function`: select the function you want to use on the test item 
- `parameter`: input parameter to use to call the function

| Test_NO |	Test_Name |	H_LMT |	L_LMT |	Test_Value | Test_Result |	Unit |	Class | Compare	| Code | Script | Function |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| 1-001 | test name | PASS | FAIL | unknow | unknow | NA | test class | EQS | E1001 | `script` | `function` |
| 1-002 | test name | PASS | FAIL | unknow | unknow | NA | test class | EQS | E1002 | `script` | `function` | 
| 1-003 | test name | PASS | FAIL | unknow | unknow | NA | test class | EQS | E1003 | `script` | `function` |

<a href="{source/vedio.mp4}" title="Link Title">



























