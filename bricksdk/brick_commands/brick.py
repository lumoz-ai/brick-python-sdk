#!/usr/bin/env python

from argparse import ArgumentParser

from bricksdk.brick_commands.command_handler import BrickCommandHandler

def brick():
    argument_parser = ArgumentParser()
    argument_parser.add_argument("command" , type = str , choices = ["create" , "initialize" , "proto"])
    argument_parser.add_argument("-i" , "--set_as_input" , action = "store_true")
    argument_parser.add_argument("-n" , "--name")
    argument_parser.add_argument("-f" , "--from-template")
    argument_parser.add_argument("-c" , "--compile" , action = "store_true")
    argument_parser.add_argument("-d" , "--download" , action = "store_true")
    command_line_arguments = argument_parser.parse_args()
    BrickCommandHandler(command_line_arguments = command_line_arguments).execute_commands()

if __name__ == '__main__':
    brick()
