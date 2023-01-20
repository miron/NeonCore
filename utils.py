import textwrap 

def wprint(text, width=80):
    wrapped_text = textwrap.wrap(text, width=width)
    for line in wrapped_text:
        print(line)
