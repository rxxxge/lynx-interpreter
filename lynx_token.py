
class Token():
    def __init__(self, tokentype, lexeme, literal, line):
        self.tokentype = tokentype
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self):
        return f"{self.tokentype} {self.lexeme} {self.literal}"
