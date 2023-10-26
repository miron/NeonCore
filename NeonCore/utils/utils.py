import textwrap


def wprint(text, width=80):
    wrapped_text = textwrap.fill(text, width=width)
    print(wrapped_text)
