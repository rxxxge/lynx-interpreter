from lynx_token import Token
from token_type import TokenType


class Scanner:
    def __init__(self, source):
        self.__tokens = []
        self.__source = source
        self._token_item = 0
        self._start = 0
        self._current = 0
        self._line = 1
        self._had_error = False
        
        self.__keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "null": TokenType.NULL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }
        
    # Support for iterators    
    def __iter__(self):
        self._token_item = 0
        return self
    
    def __next__(self):
        item = self._token_item
        if (item < len(self.__tokens)):
            self._token_item += 1
            return self.__tokens[item].to_string()
        else:
            raise StopIteration
        
        
    def error_call(self) -> bool:
        if (self._had_error):
            return True
        else:
            return False

    def error(self, line: int, message: str):
        self._report(line, "", message)
            
    def scan_tokens(self) -> list:
        while (not self._isAtEnd()):
            self._start = self._current
            self._scan_token()

        self.__tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self.__tokens

    def _scan_token(self):
        char = self._advance()
        match char:
            case '(': self._addToken(TokenType.LEFT_PAREN)    
            case ')': self._addToken(TokenType.RIGHT_PAREN)
            case '}': self._addToken(TokenType.RIGHT_BRACE)
            case '{': self._addToken(TokenType.LEFT_BRACE)
            case ',': self._addToken(TokenType.COMMA)
            case '.': self._addToken(TokenType.DOT)
            case '-': self._addToken(TokenType.MINUS)
            case '+': self._addToken(TokenType.PLUS)
            case ';': self._addToken(TokenType.SEMICOLON)
            case '*': self._addToken(TokenType.STAR)
            case '!': self._addToken(TokenType.BANG_EQUAL if self._matches('=') else TokenType.BANG)
            case '=': self._addToken(TokenType.EQUAL_EQUAL if self._matches('=') else TokenType.EQUAL)
            case '<': self._addToken(TokenType.LESS_EQUAL if self._matches('=') else TokenType.LESS)                   
            case '>': self._addToken(TokenType.GREATER_EQUAL if self._matches('=') else TokenType.GREATER)
            case '/': 
                if (self._matches('/')):
                    while (self._peek() != '\n' and not self._isAtEnd()):
                        self._advance()
                else:
                    self._addToken(TokenType.SLASH)
            case ' ': pass
            case '\r': pass
            case '\t': pass
            case '\n': self._line += 1
            case '"': 
                self._string()
            case 'o':
                if self._matches('r'):
                    self._addToken(TokenType.OR)
                    
            case _:
                if self._isDigit(char):
                    self._number()
                elif self._isAlpha(char):
                    self._identifier()
                else:
                    self.error(self._line, "Unexpected character.")

    def _report(self, line: int, where: str, message: str):
        self._had_error = True
        print(f"[line {line}] Error {where}: {message}")


    def _isAtEnd(self):
        return self._current >= len(self.__source)
    
    def _advance(self):
        char_at = self._current
        self._current += 1
        return self.__source[char_at]

    def _addToken(self, tokentype: Token):
        self._addToken_type(tokentype, None)

    def _addToken_type(self, tokentype: Token, literal):
        text = self.__source[self._start:self._current]
        self.__tokens.append(Token(tokentype, text, literal, self._line))

    def _matches(self, expected):
        if (self._isAtEnd()):
            return False
        if (self.__source[self._current] != expected):
            return False
        
        self._current += 1
        return True
    
    def _peek(self):
        if (self._isAtEnd()):
            return '\0'
        
        return self.__source[self._current]
    
    def _string(self):
        while self._peek() != '"' and not self._isAtEnd():
            if self._peek() == '\n':
                self._line += 1
            self._advance()    
                
        if self._isAtEnd():
            self.error(self._line, "Unterminated string.")
        
        self._advance()
        
        value = self.__source[self._start + 1:self._current - 1]
        self._addToken_type(TokenType.STRING, value)
        
    def _isDigit(self, char):
        return char >= '0' and char <= '9'
        
    def _number(self):
        is_float = False
        
        while self._isDigit(self._peek()):
            self._advance()
        
        if self._peek() == '.' and self._isDigit(self._peekNext()):
            is_float = True
            self._advance()
                
            
            while self._isDigit(self._peek()):
                self._advance() 
        
                
        self._addToken_type(TokenType.NUMBER, 
                             float(self.__source[self._start:self._current]) if is_float 
                             else int(self.__source[self._start:self._current]))    
        
    def _peekNext(self):
        if self._current + 1 >= len(self.__source):
            return ''
        return self.__source[self._current + 1]
    
    def _identifier(self):
        while self._isAlphaNumeric(self._peek()):
            self._advance()
            
        text = self.__source[self._start:self._current]
        parsed_type = self.__keywords[text]
        if parsed_type == None:
            parsed_type = TokenType.IDENTIFIER
        self._addToken(parsed_type)
    
    def _isAlpha(self, char):
        return  char >= 'a' and char <= 'z' or \
                char >= 'A' and char <= 'Z' or \
                char == '_'
                 
    def _isAlphaNumeric(self, char):
        return self._isAlpha(char) or self._isDigit(char)
    
        