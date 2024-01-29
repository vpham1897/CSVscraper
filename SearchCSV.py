from email.quoprimime import quote
from ensurepip import version
from re import search
from pathlib import Path
import csv
from datetime import datetime

fileName = input("Input file name \n")
while(not (Path(fileName).is_file())):
    fileName = input(fileName + " does not exist. Please input a valid file name \n")

loop = True
searchTerms = []
while(loop):
    inputtedValue = input("Enter a taxable term (\"q\" to indicate no more terms)\n")
    if(inputtedValue == "q"):
        loop = False
    else:
        searchTerms.insert(-1,inputtedValue)
#print(searchTerms)

sum = 0

loop = True
while(loop):
    availableName = input("Enter a name for output file without the .csv extension (enter nothing for default behavior)\n") + ".csv"
    if (Path(availableName).is_file()):
        loop = (input(availableName + " already exists. Proceed and override the existing file? (\"y\" to continue)\n") != "y")
    else:
        loop = False

dateRange = input("Would you like to input a date range? (\"y\"/\"n\")\n") == "y"
if(dateRange):
    loop = True
    while(loop):
        inputMin = input("Enter a min date (m/d/Y: 1/1/2000)\n")
        try:
            loop = not (bool(datetime.strptime(inputMin, '%m/%d/%Y')))
        except ValueError:
            loop = True
    dateMin = datetime.strptime(inputMin, '%m/%d/%Y').date()

    loop = True
    while(loop):
        inputMax = input("Enter a max date (m/d/Y: 12/31/2000)\n")
        try:
            loop = not (bool(datetime.strptime(inputMax, '%m/%d/%Y')))
        except ValueError:
            loop = True
    dateMax = datetime.strptime(inputMax, '%m/%d/%Y').date()


with open(fileName, newline='') as csvfile:
    
    if(availableName == ".csv"): #Default behavior
        availableName = fileName[:-4] + " modified 1.csv"
        versionNumber = 1
        while(Path(availableName).is_file()):
            versionNumber += 1
            availableName = availableName[:-5] + str(versionNumber) + ".csv"

    with open(availableName, 'w+', newline='') as exportedFile:
        currentLine = csv.reader(csvfile, delimiter=',')
        writtenFile = csv.writer(exportedFile, delimiter=",")
        for row in currentLine:
            proceed = False
            try:
                proceed = bool(datetime.strptime(row[0], '%m/%d/%Y'))
            except ValueError:
                proceed = False
            if(proceed):
                if ((not dateRange) or ((dateMin <= datetime.strptime(row[0], '%m/%d/%Y').date()) & (dateMax >= datetime.strptime(row[0], '%m/%d/%Y').date()))):
                    for term in searchTerms:
                        for column in row:
                            if(term in column):
                                print(row)
                                print("\n")
                                writtenFile.writerow(row)
                                sum += float(row[5])

print("Total sum is " + str(sum))

input("Enter a key to exit")

# Check if file name already exists then update the version accordingly
