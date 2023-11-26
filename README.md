# blockchain-node

Blockchain local node for beeline competition

In order to run application you have to own a python version of 3.11.6

# Instruction how to launch it:
1. Make local copy using git or another tools
2. Create virtual enviroment 
```
python -m venv .venv
```
3. Enter to virtual enviroment
```
.venv\Scripts\activate
```
4. Install dependencies
```
pip install -r requirements.txt
```
5. Run app
```
python main.py
```
6. Visit 127.0.0.1:5000

# Fixing some issues:
1. In case if your OS cannot enter to virtual enviroment follow this instructions:
1.1 Open Powershell with Admin
1.2 Enter this command
```
set-executionpolicy remotesigned
```
