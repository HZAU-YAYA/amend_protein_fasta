#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import argparse
import logging
import sys

LOG = logging.getLogger(__name__)
__version__ = "1.0.0"    #设置版本信息
__author__ = ("Boya Xu",)   #输入作者信息
__email__ = "xby@bioyigene.com"
__all__ = []


def add_help_args(parser):   #帮助函数
    parser.add_argument('-p', type=str, default=False, help="蛋白质文件")
    parser.add_argument('-c', type=str, default=False, help="CDS文件")
    parser.add_argument('--out', '-o', type=str, default="", help="out put file")
    return parser


def amend(protein, cds, outfile):
    w_1 = ''
    w_2 = ''
    w = ''
    with open(protein) as file_object_1:
        for line_1 in file_object_1:
            if line_1.startswith('>'):
                w_1 = line_1
            elif len(line_1) == 0:
                continue
            else:
                w_1_1 = line_1
                f = open(outfile, 'a+')
                f.write(w_1_1)
                f.close()
                continue
            with open(cds) as file_object_2:
                for line_2 in file_object_2:
                    if line_2.startswith('>'):
                        w_2 = line_2
                        p1 = re.compile(r'gene=\w+.*?')
                        p2 = re.compile(r'protein=\w+.*?')
                        p3 = re.compile(r'\w+_\d+.\d')
                        p4 = re.compile(r'\[[a-zA-Z]+\s\w+\s\w+\]')
                        p5 = re.compile(r'protein_id=\w+_\d+.\d')
                        w_2_1 = p1.findall(w_2)
                        w_2_2 = p2.findall(w_2)
                        w_2_3 = p5.findall(w_2)
                        w_1_2 = p3.findall(w_1)
                        w_1_3 = p4.findall(w_1)
                        w_1_4 = ('protein_id='+w_1_2[0])

                    else:
                        continue
                    if w_2_3[0] == w_1_4:
                        w = ('>'+w_1_2[0]+' '+'['+w_2_2[0]+']'+' '+'['+w_2_1[0]+']'+' '+w_1_3[0])
                        f = open(outfile, 'a+')
                        f.write(w+'\n')
                        f.close()
                        print(w)
                        break


def main():   #主函数，执行函数
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=''' 
name:statistic.py -- 补充蛋白质fasta文件的基因信息
attention: python amend.py -p protein.fasta -a cds.fasta -o out
version: %s
contact: %s <%s>\ 
''' % (__version__, ' '.join(__author__), __email__))
    args = add_help_args(parser).parse_args()
    amend(args.p, args.c, args.out)


if __name__ == "__main__":           #固定格式，使 import 到其他的 python 脚本中被调用（模块重用）执行
    main()
