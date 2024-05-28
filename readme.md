# BACKSTAGE
## TL;DR
This tool parses the Microsoft Backstage artifacts created by Office 2016 programs and newer. It outputs a CSV with a variety of information that can prove file existence as well as to track user activity (to some extent) within Office applications.

## Description
Microsoft Backstage is a tool that most Office programs utilize. This tool is activated wwhen you have a Office program (ie., Word, Excel, Powerpoint, etc.) and you move from the document to it's "Files" tab. When you click save as and browse to a directory to save the file, Microsfoft Backstage is the one tracking this activity. 

This can be of use in digital forensics. Fortunatley, all the data is easily parsable within several json files on the local machine. These files are found at:
```
C:\users\\\*\AppData\Local\Microsoft\Office\16.0\BackstageInAppNavCache\\\*\*\\\*.json
```

This artifact contains interesting information related to directories viewed in the Backstage view, such as:
- Container URL (directory viewed)
- Last Read Time of the Container URL
- Permissions (Folder/File creation is true/false)
- All folders and files within this container, along with metadata per each file or folder:
  - Full URL and Display Name
  - Author (I've pbserved this to be a bit buggy)
  - Last Modified TIme
  - Sharing Level Description
  - A few other details that could be handy 

It should be noted that I have not done much research on the validity of the information given within these files. Though I have reason to beleive the paths and timestamp information is accurate. The other information such as author and sharing level may be dependant on your OneDrive, Sharepoint, or even M365 configurations. 

Some day I will research this and update this readme with more accurate information. For now, use this tool and the information it provides at your own risk. 

## Setup
This is a simple python script. Set it up by downloading the files from this GitHub page. Run the following command:
```
pip install -r requirements.txt
```
I recommend always using a virtual environment for each new project to keep things clean, but that is up to you. 

## Usage
```
python3 backstage.py [-h] --drive DRIVE --output OUTPUT [--verbose]

Microsoft Backstage Parser. This will parse Microsoft Backstage files into a CSV file.

options:
  -h, --help            show this help message and exit
  --drive DRIVE, -d DRIVE
                        Drive to search. Eg: C:\
  --output OUTPUT, -o OUTPUT
                        Output path. Eg: C:\output.csv
  --verbose, -v         Enable verbose logging

Stephen Hurd | HurdDFIR | v:1.0.0
```