import re

# =================================
# 1. Lexer (어휘 분석기)
# =================================
TOKEN_TYPES = [
    ('PRINT', r'print\b'),
    ('READ', r'read\b'),
    ('IF', r'if\b'),
    ('THEN', r'then\b'),
    ('ELSE', r'else\b'),
    ('WHILE', r'while\b'),
    ('LET', r'let\b'),
    ('IN', r'in\b'),
    ('END', r'end\b'),
    ('TRUE', r'true\b'),
    ('FALSE', r'false\b'),
    ('TYPE', r'(int|bool|string)\b'),
    ('EQ', r'=='),
    ('NEQ', r'!='),
    ('LE', r'<='),
    ('GE', r'>='),
    ('ASSIGN', r'='),
    ('SEMI', r';'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('AND', r'&'),
    ('OR', r'\|'),
    ('NOT', r'!'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),
    ('LT', r'<'),
    ('GT', r'>'),
    ('STRING', r'"[^"]*"'),
    ('NUMBER', r'\d+'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('SKIP', r'[ \t\n\r]+'),
]


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


def tokenize(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for token_type, regex in TOKEN_TYPES:
            m = re.compile(regex).match(code, pos)
            if m:
                match = m.group(0)
                if token_type != 'SKIP':
                    tokens.append(Token(token_type, match))
                pos = m.end()
                break
        if not match:
            raise SyntaxError(f"어휘 오류: 알 수 없는 문자 '{code[pos]}'")
    tokens.append(Token('EOF', None))
    return tokens


# =================================
# 2. Parser (구문 분석기)
# =================================
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos]

    def match(self, token_type):
        if self.current.type == token_type:
            val = self.current.value
            self.pos += 1
            self.current = self.tokens[self.pos]
            return val
        else:
            raise SyntaxError(f"구문 오류: '{token_type}' 토큰이 예상되지만 '{self.current.type}'({self.current.value})가 입력되었습니다.")

    def program(self):
        commands = []
        while self.current.type != 'EOF':
            commands.append(self.command())
        return ('program', commands)

    def command(self):
        if self.current.type == 'TYPE':
            return self.decl()
        else:
            return self.stmt()

    def decl(self):
        var_type = self.match('TYPE')
        var_name = self.match('ID')
        init_expr = None
        if self.current.type == 'ASSIGN':
            self.match('ASSIGN')
            init_expr = self.expr()
        self.match('SEMI')
        return ('decl', var_type, var_name, init_expr)

    def decls(self):
        decls_list = []
        while self.current.type == 'TYPE':
            decls_list.append(self.decl())
        return decls_list

    def stmts(self):
        stmt_list = []
        while self.current.type not in ('RBRACE', 'END', 'EOF'):
            stmt_list.append(self.stmt())
        return stmt_list

    def stmt(self):
        if self.current.type == 'LET':
            self.match('LET')
            local_decls = self.decls()
            self.match('IN')
            body_stmts = self.stmts()
            self.match('END')
            if self.current.type == 'SEMI':
                self.match('SEMI')
            return ('let', local_decls, body_stmts)

        elif self.current.type == 'LBRACE':
            self.match('LBRACE')
            body = self.stmts()
            self.match('RBRACE')
            return ('block', body)

        elif self.current.type == 'IF':
            self.match('IF')
            self.match('LPAREN')
            cond = self.expr()
            self.match('RPAREN')
            self.match('THEN')
            then_b = self.stmt()
            else_b = None
            if self.current.type == 'ELSE':
                self.match('ELSE')
                else_b = self.stmt()
            return ('if', cond, then_b, else_b)

        elif self.current.type == 'WHILE':
            self.match('WHILE')
            self.match('LPAREN')
            cond = self.expr()
            self.match('RPAREN')
            body = self.stmt()
            return ('while', cond, body)

        elif self.current.type == 'READ':
            self.match('READ')
            var_name = self.match('ID')
            self.match('SEMI')
            return ('read', var_name)

        elif self.current.type == 'PRINT':
            self.match('PRINT')
            e = self.expr()
            self.match('SEMI')
            return ('print', e)

        elif self.current.type == 'ID':
            var_name = self.match('ID')
            self.match('ASSIGN')
            e = self.expr()
            self.match('SEMI')
            return ('assign', var_name, e)

        else:
            raise SyntaxError(f"유효하지 않은 문장 시작 토큰: '{self.current.value}'")

    def expr(self):
        if self.current.type == 'NOT':
            self.match('NOT')
            return ('not', self.expr())
        elif self.current.type == 'TRUE':
            self.match('TRUE')
            return True
        elif self.current.type == 'FALSE':
            self.match('FALSE')
            return False
        else:
            node = self.bexp()
            while self.current.type in ('AND', 'OR'):
                op = self.current.type
                self.match(op)
                right = self.bexp()
                node = (op, node, right)
            return node

    def bexp(self):
        node = self.aexp()
        if self.current.type in ('EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE'):
            op = self.match(self.current.type)
            right = self.aexp()
            node = (op, node, right)
        return node

    def aexp(self):
        node = self.term()
        while self.current.type in ('PLUS', 'MINUS'):
            op = self.match(self.current.type)
            right = self.term()
            node = (op, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.current.type in ('MUL', 'DIV'):
            op = self.match(self.current.type)
            right = self.factor()
            node = (op, node, right)
        return node

    def factor(self):
        is_neg = False
        if self.current.type == 'MINUS':
            self.match('MINUS')
            is_neg = True

        if self.current.type == 'NUMBER':
            val = int(self.match('NUMBER'))
            node = -val if is_neg else val
        elif self.current.type == 'STRING':
            val = self.match('STRING')[1:-1]
            node = val
        elif self.current.type == 'LPAREN':
            self.match('LPAREN')
            node = self.aexp()
            self.match('RPAREN')
            if is_neg: node = ('neg', node)
        elif self.current.type == 'ID':
            var_name = self.match('ID')
            node = ('id', var_name)
            if is_neg: node = ('neg', node)
        else:
            raise SyntaxError(f"Factor 파싱 오류: '{self.current.value}'")
        return node


# =================================
# 3. Interpreter (실행기)
# =================================
class Interpreter:
    def __init__(self):
        self.scopes = [{}]

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def set_var(self, name, value):
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
        self.scopes[-1][name] = value

    def get_var(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return 0

    def eval_expr(self, node):
        if isinstance(node, (bool, int, str)): return node
        if isinstance(node, tuple):
            op = node[0]
            if op == 'id': return self.get_var(node[1])
            if op == 'neg': return -self.eval_expr(node[1])
            if op == 'not': return not self.eval_expr(node[1])

            left = self.eval_expr(node[1])
            right = self.eval_expr(node[2])

            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/': return left // right
            if op == '==': return left == right
            if op == '!=': return left != right
            if op == '<': return left < right
            if op == '>': return left > right
            if op == '<=': return left <= right
            if op == '>=': return left >= right
            if op == 'AND': return left and right
            if op == 'OR': return left or right
        return 0

    def execute(self, node):
        kind = node[0]

        if kind == 'program':
            for cmd in node[1]:
                self.execute(cmd)

        elif kind == 'decl':
            _, v_type, v_name, init_expr = node
            val = self.eval_expr(init_expr) if init_expr else 0
            self.scopes[-1][v_name] = val

        elif kind == 'assign':
            v_name, expr_node = node[1], node[2]
            self.set_var(v_name, self.eval_expr(expr_node))

        elif kind == 'block':
            for s in node[1]:
                self.execute(s)

        elif kind == 'let':
            self.push_scope()
            local_decls, body_stmts = node[1], node[2]
            for d in local_decls:
                self.execute(d)
            for s in body_stmts:
                self.execute(s)
            self.pop_scope()

        elif kind == 'if':
            cond, then_b, else_b = node[1], node[2], node[3]
            if self.eval_expr(cond):
                self.execute(then_b)
            elif else_b:
                self.execute(else_b)

        elif kind == 'while':
            cond, body = node[1], node[2]
            while self.eval_expr(cond):
                self.execute(body)

        elif kind == 'read':
            v_name = node[1]
            val = int(input(f"[{v_name}] 값 입력: "))
            self.set_var(v_name, val)

        elif kind == 'print':
            val = self.eval_expr(node[1])
            print(">> [S 언어 출력]:", val)


# =================================
# 4. S 언어 코드 작성 및 실행 (내부 삽입 방식)
# =================================
if __name__ == "__main__":

    # S 언어 프로그램 작성 공간

    s_code = """

    let int x = 0; in
        x = x + 2;
       print x;
    end;

    """

    # 디버그 옵션 (필요시 True로 변경)
    SHOW_TOKENS = False
    SHOW_AST = False

    try:
        tokens = tokenize(s_code)
        if SHOW_TOKENS:
            print("=== [1] 토큰 목록 ===")
            print(tokens)
            print()

        parser = Parser(tokens)
        ast = parser.program()
        if SHOW_AST:
            print("=== [2] 추상 구문 트리 (AST) ===")
            print(ast)
            print()

        print("=== [실행 결과] ===")
        interpreter = Interpreter()
        interpreter.execute(ast)

    except Exception as e:
        print("\n[오류 발생]:", e)
