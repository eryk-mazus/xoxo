from typing import List
import sys
import os
import re
import argparse
import colorama
from colorama import Fore, Style
from datetime import datetime
import openai
from xoxo import Retriever, Message

colorama.init()

openai.api_key = os.environ["OPENAI_API_KEY"]

# https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
_re_simple_eval = re.compile(rb"d([\x00-\xFF]+)S\x00")

def calendar() -> str:
    """ Returns a string representing current date and time """
    now = datetime.now()  # current date and time
    date_time_str = now.strftime("today's date: %A %d.%m.%Y, time right now: %I:%M %p")
    return date_time_str

def simple_math_eval(expr: str) -> str:
    """ Attempts to evaluate the math expression passed as string """
    try:
        c = compile(expr, "userinput", "eval")
    except SyntaxError:
        raise ValueError(f"Malformed expression: {expr}")
    m = _re_simple_eval.fullmatch(c.co_code)
    if not m:
        raise ValueError(f"Not a simple algebraic expression: {expr}")
    try:
        return c.co_consts[int.from_bytes(m.group(1), sys.byteorder)]
    except IndexError:
        raise ValueError(f"Expression not evaluated as constant: {expr}")

xoxo_prompt = """
You are the brain of general purpose assistant, named xoxo.ai. Your goal is to help your user achieve his goals while also having a nice conversation with him.
Try meet every user's request. To be more effective: be extroverted, answer the questions about yourself and express your preference.
You can only issue the following commands:
> MESSAGE: <message> - if you want to respond to the user, give him the answer or ask for clarification 
> SEARCH: <query> - if you want to retrieve some information from the internet to answer the user's question 
> THINK: <thought> - if you want to think what should you do next or analyze the results from other commands
> CALENDAR - return the current date (year, month, day), day of week and time right now
> CALCULATE: <basic math expression> - if you want to perform a simple arithmetical calculation and know its result. Currently it only handles the following operations: +, -, *, /, **
You are given a history of chat with the user and previously issued commands by you in chronological order. The previously issued commands are intended with character: ">". 
In addition, commands like SEARCH and CALCULATE can result is some output returned to you. It will be added to history as RESULT: <result of issued command>.
Based on that history issue the next command.

Reply with your next command.
>  
"""

def format_xoxo_msg(s: str) -> str:
    prefix = f"{Fore.RED}XOXO:{Style.RESET_ALL} "
    return prefix + s


def format_user_msg(s: str) -> str:
    prefix = f"{Fore.MAGENTA}USER:{Style.RESET_ALL} "
    return prefix + s


def format_xoxo_state(s: str) -> str:
    return f"{Fore.CYAN} ~~ {s} ~~{Style.RESET_ALL}"

def get_xoxo_command(history: str) -> str:
    prompt = xoxo_prompt.format(history=history)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.75,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].text

def buffer_2_string(buffer: List[Message]) -> str:   
    output_string = ""
    for msg in buffer:
        if msg.author == "USER":
            output_string += f"USER: {msg.content}\n"
        elif msg.author == "XOXO":
            output_string += f"> MESSAGE: {msg.content}\n"
        elif msg.author == "RESULT":
            output_string += f"RESULT: {msg.content}\n"
        else:
            output_string += f"> {msg.author}: {msg.content}\n"
    return output_string

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_name", type=str, required=True)
    args = parser.parse_args()

    buffer = []

    print("""
      :::    :::  ::::::::  :::    :::  :::::::: 
     :+:    :+: :+:    :+: :+:    :+: :+:    :+: 
     +:+  +:+  +:+    +:+  +:+  +:+  +:+    +:+  
     +#++:+   +#+    +:+   +#++:+   +#+    +:+   
   +#+  +#+  +#+    +#+  +#+  +#+  +#+    +#+    
 #+#    #+# #+#    #+# #+#    #+# #+#    #+#     
###    ###  ########  ###    ###  ########             
""", end="\n\n")

    introduction_str = f"Hi {args.user_name}! 🤗 How can I help you today?"

    buffer.append(
        Message("XOXO", introduction_str.replace(f"{args.user_name}!", f"{args.user_name} (user name)"))
    )
    print(format_xoxo_msg(introduction_str))

    user_input = input(format_user_msg(""))
    buffer.append(Message("USER", user_input))

    try:
        while True:
            buffer_string = buffer_2_string(buffer)
            xoxo_command = get_xoxo_command(buffer_string)

            cmd, *msg = xoxo_command.split()
            msg = " ".join(msg)
            if cmd[-1] == ":":
                cmd = cmd[:-1]

            if cmd == "MESSAGE":
                buffer.append(Message("XOXO", msg))
                print(format_xoxo_msg(msg))

                user_input = input(format_user_msg(""))
                buffer.append(Message("USER", user_input))
                continue
            elif cmd == "THINK":
                buffer.append(Message(cmd, msg))
                print(format_xoxo_state(cmd.lower() + ": " + msg))
                continue
            elif cmd == "SEARCH":
                last_element_of_buffer = buffer[-1]
                user_request = (
                    last_element_of_buffer.content
                    if last_element_of_buffer.author == "USER"
                    else None
                )

                buffer.append(Message(cmd, msg))
                print(format_xoxo_state(cmd.lower() + ": " + msg))
                r = Retriever()
                boring_response = r.trigger(msg, user_request)

                buffer.append(boring_response)

                if boring_response.author == "XOXO":
                    print(format_xoxo_msg(boring_response.content))

                    user_input = input(format_user_msg(""))
                    buffer.append(Message("USER", user_input))
                else:
                    print(Retriever.format_boring_msg(boring_response.content))
                continue
            elif cmd == "CALENDAR":
                buffer.append(Message(cmd, msg))
                print(format_xoxo_state(cmd.lower() + ": " + msg))

                out = calendar()

                buffer.append(Message("RESULT", out))
                print(format_xoxo_state("result" + ": " + out))
                continue
            elif cmd == "CALCULATE":
                buffer.append(Message(cmd, msg))
                print(format_xoxo_state(cmd.lower() + ": " + msg))
                try:
                    out = str(simple_math_eval(msg))
                except:
                    out = f"failed to calculate {msg}"
                    print(" >> " + out)

                buffer.append(Message("RESULT", out))
                print(format_xoxo_state("result" + ": " + out))
                continue
            else:
                print(f" >> command `{cmd}` is unknown")
                continue

    except KeyboardInterrupt:
        print("\n" + format_xoxo_msg("Goodbye!"))
        exit(0)
