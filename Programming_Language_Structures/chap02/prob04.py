import re

# ==========================================
# 1. 어휘 분석기 (Lexer)
# S 언어 문장(문자열)을 의미 있는 단위(토큰)로 쪼갭니다.
# ==========================================
TOKEN_TYPES = [
    ('NUMBER', r'\d+'),  # 숫자 (예: 1, 2, 10)
    ('PLUS', r'\+'),  # +
    ('MINUS', r'-'),  # -
    ('MUL', r'\*'),  # *
    ('DIV', r'/'),  # /
    ('LPAREN', r'\('),  # (
    ('RPAREN', r'\)'),  # )
    ('SKIP', r'[ \t\n]+'),  # 공백 및 줄바꿈 (무시)
]


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"


def lex(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for token_type, regex in TOKEN_TYPES:
            regex_match = re.compile(regex).match(code, pos)
            if regex_match:
                match = regex_match.group(0)
                if token_type != 'SKIP':
                    tokens.append(Token(token_type, match))
                pos = regex_match.end()
                break
        if not match:
            raise SyntaxError(f"해석할 수 없는 문자: {code[pos]}")
    tokens.append(Token('EOF', None))
    return tokens


# ==========================================
# 2. 구문 분석기 (Parser)
# 토큰들을 규칙(BNF 문법)에 맞게 검사하며 트리(AST)로 만듭니다.
# ==========================================
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        else:
            raise SyntaxError(f"예상치 못한 토큰: {self.current_token.type}")

    # factor = NUMBER | LPAREN expr RPAREN
    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return int(token.value)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node

    # term = factor ((MUL | DIV) factor)*
    def term(self):
        node = self.factor()
        while self.current_token.type in ('MUL', 'DIV'):
            token = self.current_token
            if token.type == 'MUL':
                self.eat('MUL')
                node = ('*', node, self.factor())
            elif token.type == 'DIV':
                self.eat('DIV')
                node = ('/', node, self.factor())
        return node

    # expr = term ((PLUS | MINUS) term)*
    def expr(self):
        node = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
                node = ('+', node, self.term())
            elif token.type == 'MINUS':
                self.eat('MINUS')
                node = ('-', node, self.term())
        return node


# ==========================================
# 3. 평가기/인터프리터 (Evaluator)
# 파싱된 트리 구조를 계산하여 최종 실행 결과를 냅니다.
# ==========================================
def evaluate(node):
    if isinstance(node, int):
        return node

    op, left, right = node
    if op == '+': return evaluate(left) + evaluate(right)
    if op == '-': return evaluate(left) - evaluate(right)
    if op == '*': return evaluate(left) * evaluate(right)
    if op == '/': return evaluate(left) // evaluate(right)


# ==========================================
# 4. 실제로 S 언어 문장을 넣고 실행해보는 메인 함수
# ==========================================
if __name__ == "__main__":
    # 실행해볼 S 언어 코드
    s_code = "3 + 5 * (10 - 2)"

    print("==========================================")
    print(f" 입력받은 S 언어 문장: {s_code}")
    print("==========================================")

    # 1단계: 어휘 분석
    tokens = lex(s_code)
    print(f"\n[1단계 토큰화 결과]\n{tokens}")

    # 2단계: 구문 분석
    parser = Parser(tokens)
    ast = parser.expr()
    print(f"\n[2단계 AST 트리 구조]\n{ast}")

    # 3단계: 실행/평가
    result = evaluate(ast)
    print(f"\n[3단계 최종 실행 결과]\n{result}")
    print("==========================================")
