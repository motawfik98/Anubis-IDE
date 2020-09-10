from PyQt5.QtWidgets import QLineEdit, QDialog, QDialogButtonBox, QFormLayout, QCheckBox
import subprocess
import os

class Form(QDialog):
    def __init__(self, params, parent=None):
        super().__init__(parent)
        self.paramsLength = len(params) + 1 # get the length of the parameters
        self.values = [None] * self.paramsLength # initialize an empty array
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok, self); # add OK button

        layout = QFormLayout(self) # construct FormLayout
        for i in range(self.paramsLength - 1):
            self.values[i] = QLineEdit(self) # initialize the LineEdit
            layout.addRow(params[i], self.values[i]) # add the LineEdit object to the form
        
        self.values[-1] = QCheckBox() # add a checkbox at the end of the form
        # this checkbox allows the user to enter any type and it will be automatically casted to the correct type
        layout.addRow("Automatic Casting", self.values[-1])
        
        layout.addWidget(buttonBox) # add button to the layout

        buttonBox.accepted.connect(self.accept)
        
    # func to get the values that the user entered
    def getInputs(self):
        values = [None] * self.paramsLength
        for i in range(self.paramsLength - 1): # gets the value of each input with removing spaces
            values[i] = self.values[i].text().strip()
        values[-1] = True if self.values[-1].isChecked() else False # get the user input for the checkbox
        return values

    
class FastRun():
    def __init__(self, code, params):
        super().__init__()
        self.code = code
        self.params = params
        form = Form(params) # initialize Form to appear to the user
        if form.exec(): # wait till the user presses OK
            self.userValues = form.getInputs() # get the values that the user entered
            self.formatTypes() # format these values to put them in a file

    def createFastRunFile(self):
        file = open('fastFunction.py', 'w+') # create new file
        file.write("def main():\n") # add declaration for main function
        for i in range(len(self.params)): # loop over the params
            # type the parameter name with its value
            file.write(f'\t{self.params[i]} = {self.userValues[i]}\n')
        
        file.write('\n')
        for line in self.code: # write the code line by line
            file.write(line + "\n")
        file.write("\n\nmain()\n") # call main function
        file.close()

        os.system("python3 fastFunction.py > output.log") # run the file and redirect the output to another file
        # os.remove("fastFunction.py") # delete the file as it has no use now
        # the file won't be deleted to view its content

    def formatTypes(self):
        for i in range(len(self.userValues) - 1): # loop over the values that the user entered
            if self.isFloat(self.userValues[i]) and self.userValues[-1]: # check if it's float and the user checked the casting checkbox
                self.userValues[i] = float(self.userValues[i]) # convert the param to float
                continue
            if self.isBool(self.userValues[i]) and self.userValues[-1]: # check if it's a boolean and the user checked the casting checkbox
                self.userValues[i] = self.convertToBool(self.userValues[i]) # convert the param to bool
                continue
            self.userValues[i] = f'"""{self.userValues[i]}"""' # if it's a string then add quotes around it to be in the correct format when declared
            

    # function to check if the value is float
    def isFloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    # function to check if the value is bool
    def isBool(self, value):
        if value.lower() == 'true' or value.lower() == 'false':
            return True
        return False

    # get the bool value from its string value
    def convertToBool(self, value):
        if value.lower() == 'true':
            return True
        return False