#!/usr/bin/env python
'''Returns color-schemed ASCII art heading --> RADIO. \
dark cyan --> '\x1b[38;2;72;201;176m' \
yellow --> '\x1b[38;2;244;208;63m' \
dark orange --> '\x1b[38;2;220;118;51m' \
reset --> '\x1b[0m' '''


def get_ascii_art():
    '''Get ASCII art.'''
    radio = '''\x1b[38;2;72;201;176m
:::::::..    :::.   :::::::-.  :::    ...
;;;;``;;;;   ;;`;;   ;;,   `';,;;; .;;;;;;;.\x1b[38;2;244;208;63m
 [[[,/[[['  ,[[ '[[, `[[     [[[[[,[[     \\[[,
 $$$$$$c   c$$$cc$$$c $$,    $$$$$$$$,     $$$\x1b[38;2;220;118;51m
 888b "88bo,888   888,888_,o8P'888"888,_ _,88P
 MMMM   "W" YMM   ""` MMMMP"`  MMM  "YMMMMMP"\x1b[0m'''

    return radio  # return ASCII art heading


if __name__ == '__main__':
    get_ascii_art()
