#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: Wu Zihao
# time: 2019/10/8
# function:

import sys
import os
import question


def random_exercises(q_c, m_v):
    """
    根据输入的题目数量和数字范围，生成题目文件和答案文件
    :param q_c: 题目数量
    :param m_v: 数字最大值
    :return: 在目录下生成试题文件和答案文件
    """
    e_open = open("Exercises.txt", "a+")
    a_open = open("Answers.txt", "a+")
    for i in range(0, q_c):
        post = question.post_order_generator(m_v)
        tree = question.post_to_tree(post)
        ordinary = question.tree_to_ordinary(tree, [])
        readable_str = question.to_readable(ordinary)
        e_open.write(f'{i+1}、{readable_str}\n')

        answer = question.count_ans(post)
        a_open.write(f'{i+1}、{answer}\n')
    e_open.close()
    a_open.close()


def make_standard(e_p):
    """
    根据题目文件生成标准答案StandardAnswers.txt
    :param e_p: 题目文件的path
    :return: 生成StandardAnswers.txt
    """
    try:
        e_open = open(e_p, "r")
    except FileNotFoundError:
        print("找不到该文件")
        sys.exit()
    except:
        print("文件打开失败，请重新运行程序")
        sys.exit()
    sa_open = open("StandardAnswers.txt", "a+")
    e_lines = e_open.readlines()
    for line in e_lines:
        ques_num = line.split("、")[0]  # 题目序号
        ques_str = line.split("、")[1].rstrip('\n')  # 去掉前面的序号和后面换行符
        ordinary = question.to_unreadable(ques_str)
        post = question.ordinary_to_post(ordinary)
        sa = question.count_ans(post)
        sa_open.write(f'{ques_num}、{sa}\n')

    e_open.close()
    sa_open.close()


def check_exercise(a_p):
    """
    标准答案与用户答案逐行对比，统计对错
    :param a_p: 用户答案path
    :return: 生成Grade.txt统计文件
    """
    sa_open = open("StandardAnswers.txt", "r")
    a_open = open(a_p, "r")
    sa_lines = sa_open.readlines()
    right = []
    wrong = []

    for sa_line in sa_lines:
        if sa_line == a_open.readline():
            right.append(sa_line.split("、")[0])
        else:
            wrong.append(sa_line.split("、")[0])
    sa_open.close()
    a_open.close()

    grade_open = open("Grade.txt", "a+")
    grade_open.write(f'正确{len(right)}题：{right}\n')
    grade_open.write(f'错误{len(wrong)}题：{wrong}\n')


if __name__ == '__main__':
    print('''
************************************************************
***               功能: 生成小学四则运算题目             ***
************************************************************
------------------------------------------------------------
生成题目模式：
    Myapp.exe -n <number> -r <range>
    生成number道范围在range的题目
批改题目模式：
    Myapp.exe -e <exercisefile>.txt -a <answerfile>.txt
    对题目文件txt和用户答案txt进行对比，输出答题情况
------------------------------------------------------------
用法示例：
    Myapp.exe -n 10 -r 20
    生成10道20以内的题目
    Myapp.exe -e C:/题目.txt -a D:/答案.txt
    对C盘下的题目和D盘下的答案对比
------------------------------------------------------------
版本：--v1.0  2019-10-11 17:29:23
作者：Li Guangzheng     3117004660
　　　Wu Zihao          3117004671
------------------------------------------------------------
毛主席语录：好好学习，天天向上
------------------------------------------------------------
            ''')

    if len(sys.argv) != 5:
        print("请参照上面的说明,使用正确的参数重新运行程序")
        sys.exit()

    if sys.argv[1] == '-n':  # 生成模式
        ques_count = int(sys.argv[2])
        max_val = int(sys.argv[4])
        random_exercises(ques_count, max_val)
        print('''
------------------------------------------------------------
提示：题目生成完毕！快为建设社会主义事业而奋斗！
------------------------------------------------------------
                    ''')
    elif sys.argv[1] == '-e':  # 批改模式
        exercise_path = os.path.abspath(sys.argv[2])
        answer_path = os.path.abspath(sys.argv[4])
        make_standard(exercise_path)
        check_exercise(answer_path)
        print('''
------------------------------------------------------------
提示：答案批改完毕！实践是检验真理的唯一标准！
------------------------------------------------------------
                    ''')
    else:
        print("请参照上面的说明,使用正确的参数重新运行程序")
        sys.exit()

