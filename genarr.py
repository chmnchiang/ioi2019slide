class Cols:
    def __init__(self, C):
        self.C = C

    def __str__(self):
        return ' & '.join(str(x) for x in self.C)

class Rows:
    def __init__(self, R):
        self.R = R

    def __str__(self):
        return '\\begin{bmatrix}\n' + ''.join(
            str(r) + ' \\\\ \n' for r in self.R
        ) + '\\end{bmatrix}\n'

class Wrap:
    def __init__(self, name, cont):
        self.name = name
        self.cont = cont

    def __str__(self):
        return f'\\{self.name}{{{self.cont}}}'

def Alert(r, c):
    return Wrap(f'alert<{r}>', c)

def excf(x):
    y = 0
    def ret():
        nonlocal y
        y = y + 1
        if not y:
            return ''
        else:
            return x
    return ret


adv = excf('\\myaddv')

F = Rows([ str(x) + adv() for x in [
    Alert('2-3', 'f(x_0)'), 
    Alert('2-', 'f(x_1)'), 
    Alert('2-', 'f(x_2)'), 
    Alert('2-3', 'f(x_3)'), 
    Alert('2-3', '\\vdots'), 
    Alert('2-3', 'f(x_{m-1})'),
    '\\vdots',
    'f(x_n)',
]])

adv = excf('\\myaddv')

A = Rows([str(x) + '\\myaddv' for x in [ 
    Alert('2-3', 'a_0'),
    Alert('4-', 'a_1'),
    Alert('2-3', 'a_2'),
    Alert('4-', 'a_3'),
    Alert('2-3', '\\vdots'),
    Alert('2-3', 'a_{n-2}'),
    Alert('4-', 'a_{n-1}'),
]])

def what(i, j):
    if i == 4 or i == 6:
        if j == 4:
            return '\\ddots'
        else:
            return '\\vdots'

    if j == 4:
        return '\\hdots'

    if i*j == 0:
        return '1'

    if i < 4:
        q = '' if i == 1 else str(i)
        if j < 4:
            return f'\\omega_n^{{ {"" if i*j == 1 else i*j} }}'
        elif j == 5:
            return f'\\omega_n^{{ {q}(n-2) }}'
        elif j == 6:
            return f'\\omega_n^{{ {q}(n-1) }}'

    if i == 5:
        y = '(m-1)'
    elif i == 7:
        y = '(n-1)'

    if j == 0:
        z = ''
    elif j == 5:
        z = '(n-2)'
    elif j == 6:
        z = '(n-1)'
    else:
        z = '' if j == 1 else str(j)

    if j >= 5:
        fin = f'\\omega_n^{{ {y}{z} }}'
    else:
        fin = f'\\omega_n^{{ {z}{y} }}'

    if j == 5 and i == 5:
        fin = '\\phantom{\\omega_n^{(m-1)(m-1)}}\\mathllap{' + fin + '}'
    if j == 6 and i == 5:
        fin = '\\phantom{\\omega^2 \\cdot \\omega_m^{2(m-1)}}\\mathllap{' + fin + '}'
    if j == 3 and i == 5:
        fin = '\\phantom{\\omega^2 \\cdot \\omega_n^{2} \omega}\\mathllap{' + fin + '}'
    return fin


def blueonly(d, x):
    return f'\\alt{d}{{\\textcolor{{blue}}{{{x}}}}}{{{x}}}'


rw = []
for i in range(8):
    cl = []
    for j in range(7):
        x = what(i, j)
        y = None
        y2 = None
        if 1 <= i <= 3:
            g = "" if i == 1 else str(i)
            if j == 2:
                y = f'\\omega_{{{blueonly("<3>", "m")}}}^{{ {blueonly("<3>", g)} }}'
            if j == 5:
                y = f'\\omega_{{{blueonly("<3>", "m")}}}^{{ {blueonly("<3>", g+"(m-1)")} }}'
        if 1 <= i <= 2:
            if i == 1:
                q = '\\textcolor{blue}{\\omega_n} \\cdot'
            else:
                q = '\\textcolor{blue}{\\omega_n^2} \\cdot'

            if j == 1:
                y2 = q + f'\\textcolor{{blue}}{1}'
            if j == 3:
                y2 = q + f'\\omega_{{\\textcolor{{blue}}{{m}}}}^{{\\textcolor{{blue}}{{ {i} }}}}'
            if j == 6:
                y2 = q + f'\\omega_{{\\textcolor{{blue}}{{m}}}}^{{\\textcolor{{blue}}{{ (m-1) }}}}'
        if i == 5:
            if j == 2:
                k = "(m-1)\\phantom{2}"
                y = f'\\omega_{{{blueonly("<3>", "m")}}}^{{ {blueonly("<3>", k)} }}'
            if j == 5:
                y = f'\\omega_{{{blueonly("<3>", "m")}}}^{{ {blueonly("<3>", "(m-1)(m-1)")} }}'
        if y is not None:
            x = Wrap('alt<3->', y + '}{' + x)

        if y2 is not None:
            x = Wrap('alt<5->', y2 + '}{' + x)

        if i <= 5 and j in (0, 2, 4, 5):
            x = Alert('2-3', x)
        if 1 <= i <= 2 and j in (1, 3, 4, 6):
            x = Alert('4-', x)
        cl.append(x)
    rw.append(Cols(cl))

M = Rows(rw)

print(f'\[ \scalebox{{0.75}}{{$ {F} = {M} {A} $}} \]')
