import time
from random import randint

'''
根据时间戳得到加密验证码， 反解之后得到生成时间
'''

def encrpto():
    s = str(time.time())
    t = s.split('.')[0]  # 取整数，秒
    print(t)
    random_seed = str(randint(0,9))
    t = t[::-1]
    a_ = t[:2]
    b_ = random_trans(random_seed, t[4:])
    c_ = t[2:4][::-1]
    d_ = random_seed
    t = a_ + b_ + c_ + d_
    return t

def dencrpto(code):
    # t = a_ + b_ + c_ + d_
    a_ = code[:2]
    b_ = code[2:8]
    c_ = code[8:-1]
    d_ = code[-1]
    random_seed = d_
    trans_part = reverse_map(random_seed, b_)
    out = a_ + c_[::-1] +trans_part 
    out = out[::-1]

    return out

def random_trans(seed, s):
    if seed == '0':
        s = s.replace('1', 'x')
        s = s.replace('2', 'z')
        s = s.replace('3', 'q')
        s = s.replace('4', 'e')
        s = s.replace('5', 'r')
        s = s.replace('6', 'h')
        s = s.replace('7', 'b')
        s = s.replace('8', 'v')
        s = s.replace('9', 'c')
        s = s.replace('0', 'a')
        return s

    elif seed == '1':
        s = s.replace('1', 'a')
        s = s.replace('2', 'c')
        s = s.replace('3', 'v')
        s = s.replace('4', 'r')
        s = s.replace('5', 'y')
        s = s.replace('6', 'm')
        s = s.replace('7', 'j')
        s = s.replace('8', 'i')
        s = s.replace('9', 'o')
        s = s.replace('0', 'p')
        return s

    elif seed == '2':
        s = s.replace('1', 'b')
        s = s.replace('2', 'n')
        s = s.replace('3', 'v')
        s = s.replace('4', 's')
        s = s.replace('5', 'x')
        s = s.replace('6', 'k')
        s = s.replace('7', 'j')
        s = s.replace('8', 'i')
        s = s.replace('9', 'f')
        s = s.replace('0', 'l')
        return s

    elif seed == '3':
        s = s.replace('1', 'b')
        s = s.replace('2', 'n')
        s = s.replace('3', 'v')
        s = s.replace('4', 's')
        s = s.replace('5', 'x')
        s = s.replace('6', 'y')
        s = s.replace('7', 'j')
        s = s.replace('8', 'i')
        s = s.replace('9', 'k')
        s = s.replace('0', 'l')
        return s

    elif seed == '4':
        s = s.replace('1', 'b')
        s = s.replace('2', 'n')
        s = s.replace('3', 'v')
        s = s.replace('4', 's')
        s = s.replace('5', 'x')
        s = s.replace('6', 'w')
        s = s.replace('7', 'u')
        s = s.replace('8', 'i')
        s = s.replace('9', 't')
        s = s.replace('0', 'l')
        return s

    if seed == '5':
        s = s.replace('1', 'p')
        s = s.replace('2', 'w')
        s = s.replace('3', 'q')
        s = s.replace('4', 'e')
        s = s.replace('5', 't')
        s = s.replace('6', 'm')
        s = s.replace('7', 'u')
        s = s.replace('8', 'r')
        s = s.replace('9', 'c')
        s = s.replace('0', 'a')
        return s

    elif seed == '6':
        s = s.replace('1', 'a')
        s = s.replace('2', 'c')
        s = s.replace('3', 'v')
        s = s.replace('4', 'r')
        s = s.replace('5', 'y')
        s = s.replace('6', 'k')
        s = s.replace('7', 'j')
        s = s.replace('8', 'i')
        s = s.replace('9', 'o')
        s = s.replace('0', 'p')
        return s

    elif seed == '7':
        s = s.replace('1', 'b')
        s = s.replace('2', 'n')
        s = s.replace('3', 'v')
        s = s.replace('4', 's')
        s = s.replace('5', 'x')
        s = s.replace('6', 'p')
        s = s.replace('7', 'j')
        s = s.replace('8', 'i')
        s = s.replace('9', 'g')
        s = s.replace('0', 'l')
        return s

    elif seed == '8':
        s = s.replace('1', 'b')
        s = s.replace('2', 'n')
        s = s.replace('3', 'v')
        s = s.replace('4', 's')
        s = s.replace('5', 'x')
        s = s.replace('6', '3')
        s = s.replace('7', 'j')
        s = s.replace('8', 'i')
        s = s.replace('9', 't')
        s = s.replace('0', 'm')
        return s

    elif seed == '9':
        s = s.replace('1', 'b')
        s = s.replace('2', 'n')
        s = s.replace('3', 'v')
        s = s.replace('4', 's')
        s = s.replace('5', 'x')
        s = s.replace('6', '1')
        s = s.replace('7', 'j')
        s = s.replace('8', 'i')
        s = s.replace('9', 'm')
        s = s.replace('0', 'o')
        return s


def reverse_map(seed, s):
    if seed == '0':
        s = s.replace('x','1')
        s = s.replace('z','2')
        s = s.replace('q','3')
        s = s.replace('e','4')
        s = s.replace('r','5')
        s = s.replace('h','6')
        s = s.replace('b','7')
        s = s.replace('v','8')
        s = s.replace('c','9')
        s = s.replace('a','0')
        return s

    elif seed == '1':
        s = s.replace('a','1')
        s = s.replace('c','2')
        s = s.replace('v','3')
        s = s.replace('r','4')
        s = s.replace('y','5')
        s = s.replace('m','6')
        s = s.replace('j','7')
        s = s.replace('i','8')
        s = s.replace('o','9')
        s = s.replace('p','0')
        return s

    elif seed == '2':
        s = s.replace('b','1')
        s = s.replace('n','2')
        s = s.replace('v','3')
        s = s.replace('s','4')
        s = s.replace('x','5')
        s = s.replace('k','6')
        s = s.replace('j','7')
        s = s.replace('i','8')
        s = s.replace('f','9')
        s = s.replace('l','0')
        return s

    elif seed == '3':
        s = s.replace('b','1')
        s = s.replace('n','2')
        s = s.replace('v','3')
        s = s.replace('s','4')
        s = s.replace('x','5')
        s = s.replace('y','6')
        s = s.replace('j','7')
        s = s.replace('i','8')
        s = s.replace('k','9')
        s = s.replace('l','0')
        return s

    elif seed == '4':
        s = s.replace('b','1')
        s = s.replace('n','2')
        s = s.replace('v','3')
        s = s.replace('s','4')
        s = s.replace('x','5')
        s = s.replace('w','6')
        s = s.replace('u','7')
        s = s.replace('i','8')
        s = s.replace('t','9')
        s = s.replace('l','0')
        return s

    if seed == '5':
        s = s.replace('p','1')
        s = s.replace('w','2')
        s = s.replace('q','3')
        s = s.replace('e','4')
        s = s.replace('t','5')
        s = s.replace('m','6')
        s = s.replace('u','7')
        s = s.replace('r','8')
        s = s.replace('c','9')
        s = s.replace('a','0')
        return s

    elif seed == '6':
        s = s.replace('a','1')
        s = s.replace('c','2')
        s = s.replace('v','3')
        s = s.replace('r','4')
        s = s.replace('y','5')
        s = s.replace('k','6')
        s = s.replace('j','7')
        s = s.replace('i','8')
        s = s.replace('o','9')
        s = s.replace('p','0')
        return s

    elif seed == '7':
        s = s.replace('b','1')
        s = s.replace('n','2')
        s = s.replace('v','3')
        s = s.replace('s','4')
        s = s.replace('x','5')
        s = s.replace('p','6')
        s = s.replace('j','7')
        s = s.replace('i','8')
        s = s.replace('g','9')
        s = s.replace('l','0')
        return s

    elif seed == '8':
        s = s.replace('b','1')
        s = s.replace('n','2')
        s = s.replace('v','3')
        s = s.replace('s','4')
        s = s.replace('x','5')
        s = s.replace('3','6')
        s = s.replace('j','7')
        s = s.replace('i','8')
        s = s.replace('t','9')
        s = s.replace('m','0')
        return s

    elif seed == '9':
        s = s.replace('b','1')
        s = s.replace('n','2')
        s = s.replace('v','3')
        s = s.replace('s','4')
        s = s.replace('x','5')
        s = s.replace('1','6')
        s = s.replace('j','7')
        s = s.replace('i','8')
        s = s.replace('m','9')
        s = s.replace('o','0')
        return s




