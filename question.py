from fractions import Fraction
import random

# set全局变量，用来判断随机出来的表达式是否出现过
problem_set = set()


def to_with_fraction(s):
    """
    把分数转换成带分数
    :param s:普通分数形式的str类型
    :return:带分数形式的str类型
    """
    fra = Fraction(s)
    if fra.denominator != 1 and fra.numerator > fra.denominator:
        temp = fra.numerator // fra.denominator   # 整数部分
        fra = fra - temp  # 真分数部分
        return "'".join([str(temp), str(fra)])
    else:
        return s


def to_fraction(s):
    """
    带分数转换成普通分数
    :param s: 带分数形式的str类型
    :return: 普通分数的str类型
    """
    if "'" in s:
        temp = s.split("'")
        return str(int(temp[0]) + Fraction(temp[1]))
    else:
        return s


def get_random_fraction(max_value):
    """
    随机获得一个随机分数，分子分母均小于max_value
    :param max_value: int类型
    :return: Fraction类型的分数
    """
    return Fraction(random.randrange(0, max_value), random.randrange(1, max_value))


def count_ans(post_list):
    """
    计算逆波兰式的结果和判断这条式子是否合法，
    如果中途出现负数或者除零都会返回-1，否则返回最终结果
    :param post_list: 逆波兰式的列表
    :return: Fraction类型的结果
    """
    ch = ('+', '-', '×', '÷')
    stack = []
    for v in post_list:
        if v in ch:
            t1, t2 = stack.pop(), stack.pop()
            try:
                if v == '+':
                    t1 = t1 + t2
                elif v == '-':
                    t1 = t2 - t1
                elif v == '×':
                    t1 = t1 * t2
                else:
                    t1 = t2 / t1
                if t1 < 0:
                    return -1
                stack.append(t1)
            except ZeroDivisionError:
                return -1
        else:
            stack.append(Fraction(v))
    return stack[0]


def post_order_generator(max_value):
    """
    逆波兰式子生成器，随机生成一个逆波兰表达式
    :param max_value: int类型，表示数值的最大值
    :return: 存储逆波兰表达式的列表
    """
    ch = ('+', '-', '×', '÷')
    char_num = random.randrange(1, 4)
    num_num = char_num - 1
    # suffix_list是逆波兰表达式列表，先在列表前面插入两个数字
    suffix_list = [str(get_random_fraction(max_value)), str(get_random_fraction(max_value))]
    now_num = 2
    while char_num or num_num:
        if now_num >= 2:
            if char_num and random.randrange(0, 2):
                suffix_list.append(ch[random.randrange(0, 4)])
                now_num = now_num - 1
                char_num = char_num - 1
            elif num_num:
                suffix_list.append(str(get_random_fraction(max_value)))
                num_num = num_num - 1
                now_num = now_num + 1
            else:
                suffix_list.append(ch[random.randrange(0, 4)])
                char_num = char_num - 1
                now_num = now_num - 1
        else:
            suffix_list.append(str(get_random_fraction(max_value)))
            now_num = now_num + 1
            num_num = num_num - 1
    st = ".".join(suffix_list)
    if st in problem_set or count_ans(suffix_list) < 0:
        suffix_list = post_order_generator(max_value)
        return suffix_list
    else:
        problem_set.add(st)
        return suffix_list


def post_to_tree(post_list):
    """
    把逆波兰式转换成一棵模拟二叉树
    :param post_list: 逆波兰式列表
    :return: 一个列表，表示一棵树
    """
    ch = ('+', '-', '×', '÷')
    temp = []
    for v in post_list:
        if v in ch:
            t1, t2 = temp.pop(), temp.pop()
            temp.append([t2, t1, v])
        else:
            temp.append(v)
    return temp[0]


def tree_to_ordinary(tree_list, medium_list):
    """
    把二叉树转换成普通表达式
    :param tree_list: 二叉树的列表
    :param medium_list:中序表达式的列表，主要为了递归调用，刚开始可传一个空列表
    :return:一个普通表达式的列表
    """
    ch_val = {'+': 1, '-': 1, '×': 2, '÷': 2}  # 符号优先级
    if type(tree_list[0]) == list:
        if ch_val[tree_list[2]] > ch_val[tree_list[0][2]]:
            medium_list.append('(')
            medium_list = tree_to_ordinary(tree_list[0], medium_list)
            medium_list.append(')')
        else:
            medium_list = tree_to_ordinary(tree_list[0], medium_list)
    else:
        medium_list.append(tree_list[0])
    medium_list.append(tree_list[2])
    if type(tree_list[1]) == list:
        medium_list.append('(')
        medium_list = tree_to_ordinary(tree_list[1], medium_list)
        medium_list.append(')')
    else:
        medium_list.append(tree_list[1])
    return medium_list


def ordinary_to_post(medium_list):
    """
    普通表达式的列表转换成后缀表达式的列表
    :param medium_list: 普通表达式的列表
    :return: 后缀表达式的列表
    """
    ch = ('+', '-', '×', '÷')
    ch_val = {'+': 1, '-': 1, '×': 2, '÷': 2}
    ts, post_list = [], []
    for u in medium_list:
        if u == '(':
            ts.append(u)
        elif u == ')':
            while 1:
                v = ts.pop()
                if v in ch:
                    post_list.append(v)
                else:
                    break
        elif u in ch:
            while len(ts):
                if ts[-1] == '(':
                    break
                elif ch_val[ts[-1]] >= ch_val[u]:
                    post_list.append(ts.pop())
                else:
                    break
            ts.append(u)
        else:
            post_list.append(u)
    while len(ts):
        post_list.append(ts.pop())
    return post_list


def to_readable(ordinary):
    """
    将假分数化为带分数，
    并将列表形式的中序算式转化为字符串形式
    :param ordinary: 中序的列表
    :return: 小学生一眼就懂的str
    """
    temp = []
    ch = ('+', '-', '×', '÷', '(', ')')
    for item in ordinary:
        if item in ch:
            temp.append(item)
        else:
            temp.append(to_with_fraction(item))
    readable_str = " ".join(temp)
    return readable_str


def to_unreadable(readable_str):
    """
    将用带分数的str式子
    转化为假分数的列表形式的中序算式
    :param readable_str: 可读的str式子
    :return: 中序算式列表
    """
    medium_list = []
    ch = ('+', '-', '×', '÷', '(', ')')
    temp = readable_str.split(" ")
    for item in temp:
        if item in ch:
            medium_list.append(item)
        else:
            medium_list.append(to_fraction(item))
    return medium_list
