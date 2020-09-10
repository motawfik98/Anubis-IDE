class FastRun:
    def __init__(self, code, params):
        self.code = code
        self.params = params

    def createFastRunFile(self):
        file = open('fastFunction.py', 'w+')
        file.write("def main():\n")
        for param in self.params:
            file.write('\t' + param + ' = input()\n')
        
        file.write('\n')
        for line in self.code:
            file.write(line + "\n")
        file.write("\n\nmain()\n")
        file.close()
