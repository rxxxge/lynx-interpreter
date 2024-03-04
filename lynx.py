import sys

from scanner import Scanner


# Lynx type
class Lynx:
    # API
    def __init__(self):
        self._termination_error = False
        
    def run_file(self, path: str):
        with open(path, 'rb') as lynx_file:
            self._run(lynx_file.read().decode('utf-8'))

    def run_prompt(self):
        while True:
            line = input(">> ")
            if (line == ''):
                break
            self._run(line)


    # ==============================
    def _run(self, source: str):
        scanner = Scanner(source)
        scanner.scan_tokens()
        if (scanner.error_call()):
            sys.exit(65)
        # print(tokens)
      
        try:
            it = iter(scanner)
            for i in it:
                print(i)
        except StopIteration:
            pass
        

# Run
lynx = Lynx()


if (len(sys.argv) > 2):
    print("Usage: lynx [script]")
    sys.exit(64)
elif (len(sys.argv) == 2):
    lynx.run_file(sys.argv[1]) 
else:
    lynx.run_prompt()


