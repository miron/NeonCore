import cmd
import sys
import asyncio
import string

from typing import Optional
# Lazy import attempt
try:
    import readline
    if not hasattr(readline, "backend"):
        readline.backend = "pyreadline3"
except ImportError:
    readline = None

class AsyncCmd:
    """
    A minimal async replacement for cmd.Cmd.
    It supports:
    - async do_* methods
    - command completion (synchronous)
    - GameIO abstraction for input/output
    """
    prompt = "(Cmd) "
    intro = None
    doc_header = "Documented commands (type help <topic>):"
    ruler = "="
    
    def __init__(self, io: GameIO):
        self.io = io
        self.lastcmd = ""
        # The cmd module uses 'identchars' to determine what counts as a command name.
        self.identchars = string.ascii_letters + string.digits + '_'
        self.completion_matches = []

    async def cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.
        """
        self.preloop()
        
        # Set up readline completer if available
        # Fallback: Check if readline is loaded elsewhere (e.g. ActionManager)
        global readline
        if readline is None and 'readline' in sys.modules:
            readline = sys.modules['readline']

        if readline:
            self.old_completer = readline.get_completer()
            readline.set_completer(self.complete)
            readline.parse_and_bind("tab: complete")
        
        if intro is not None:
            self.intro = intro
        if self.intro:
            await self.io.send(self.intro)
            
        # REGISTER AS ACTIVE HANDLER FOR COMPLETIONS
        # This ensures that if this runs as a sub-shell (nested),
        # the IO knows to ask THIS instance for completions, not the parent.
        old_handler = getattr(self.io, "cmd_handler", None)
        if hasattr(self.io, "set_cmd_handler"):
            self.io.set_cmd_handler(self)

        stop = None
        try:
            while not stop:
                if await self.precmd(self.lastcmd): # Hook for pre-command logic
                     pass 
    
                try:
                    line = await self.io.prompt(self.prompt)
                except EOFError:
                    line = "EOF"
                
                line = await self.precmd(line)
                stop = await self.onecmd(line)
                stop = await self.postcmd(stop, line)
        finally:
            # RESTORE PREVIOUS HANDLER
            if hasattr(self.io, "set_cmd_handler"):
                self.io.set_cmd_handler(old_handler)
            
        self.postloop()

        # Restore readline completer
        if readline:
            readline.set_completer(self.old_completer)

    async def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt."""
        cmd, arg, line = self.parseline(line)
        if not line:
            return await self.emptyline()
        
        if cmd is None:
            return await self.default(line)
            
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
            return True
            
        if cmd == '':
            return await self.default(line)
            
        try:
            func = getattr(self, 'do_' + cmd)
        except AttributeError:
            return await self.default(line)
            
        if asyncio.iscoroutinefunction(func):
            return await func(arg)
        else:
            return func(arg)

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple (command, args, line).
        """
        line = line.strip()
        if not line:
            return None, None, line
        elif line[0] == '?':
            line = 'help ' + line[1:]
        elif line[0] == '!':
            if hasattr(self, 'do_shell'):
                line = 'shell ' + line[1:]
            else:
                return None, None, line
                
        i, n = 0, len(line)
        while i < n and line[i] in self.identchars: 
            i += 1
        cmd, arg = line[:i], line[i:].strip()
        return cmd, arg, line

    async def emptyline(self):
        """Called when an empty line is entered in response to the prompt.
        If this method is not overridden, it repeats the last nonempty
        command entered.
        """
        if self.lastcmd:
            return await self.onecmd(self.lastcmd)

    async def default(self, line):
        """Called on an input line when the command prefix is not recognized."""
        await self.io.send(f"*** Unknown syntax: {line}")

    async def precmd(self, line):
        """Hook method executed just before the command line is
        interpreted, but after the input prompt is generated and issued.
        """
        return line

    async def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""
        return stop

    def preloop(self):
        """Hook method executed once when the cmdloop() method is called."""
        pass

    def postloop(self):
        """Hook method executed once when the cmdloop() method is about to return."""
        pass
        
    async def async_columnize(self, list, displaywidth=80):
        """Async version of columnize"""
        if not list:
            return
        
        # Simple column formatting logic
        # Assume 80 char width for now
        col_width = max(len(str(x)) for x in list) + 2
        cols = max(1, displaywidth // col_width)
        
        rows = (len(list) + cols - 1) // cols
        
        lines = []
        for row in range(rows):
            line_items = []
            for col in range(cols):
                idx = row + col * rows
                if idx < len(list):
                    line_items.append(f"{list[idx]:<{col_width}}")
            lines.append("".join(line_items))
            
        await self.io.send("\n".join(lines))

    def columnize(self, list, displaywidth=80):
        """Legacy sync columnize - warns or passes"""
        pass
         
    # Completion - Keep synchronous common with cmd
    def completenames(self, text: str, *ignored) -> list[str]:
        dotext = 'do_' + text
        names = self.get_names()
        candidates = [a[3:] + ' ' for a in names if a.startswith(dotext)]
        return candidates
        
    def get_names(self):
        # type: () -> list[str]
        return dir(self.__class__)

    async def get_completions(self, text: str, line: str, begidx: int, endidx: int) -> list[str]:
        """
        Public API to get completions without relying on readline globals.
        Used by remote clients (via WebSocket) or prompt_toolkit.
        """
        if begidx > 0:
            cmd, args, _ = self.parseline(line)
            if cmd == '':
                compfunc = self.completedefault
            else:
                try:
                    compfunc = getattr(self, 'complete_' + cmd)
                except AttributeError:
                    compfunc = self.completedefault
        else:
            compfunc = self.completenames

        res = compfunc(text, line, begidx, endidx)
        return res

    def complete(self, text, state):
        """Return the next possible completion for 'text'.
        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """
        if state == 0:
            if readline:
                origline = readline.get_line_buffer()
                line = origline.lstrip()
                stripped = len(origline) - len(line)
                begidx = readline.get_begidx() - stripped
                endidx = readline.get_endidx() - stripped
                
                # Use the new helper but execute synchronously because readline expects it
                # Note: completenames is synchronous, so most completion logic is synchronous.
                # If we had async completion logic, we'd need to loop run_until_complete here, which is risky.
                # For now, we assume all completion logic (checking dict keys) is synchronous.
                if begidx > 0:
                     cmd, args, _ = self.parseline(line)
                     if cmd == '':
                         compfunc = self.completedefault
                     else:
                         try:
                             compfunc = getattr(self, 'complete_' + cmd)
                         except AttributeError:
                             compfunc = self.completedefault
                else:
                     compfunc = self.completenames
                
                self.completion_matches = compfunc(text, line, begidx, endidx)
            else:
                pass # Can't complete without readline

        try:
            return self.completion_matches[state]
        except IndexError:
            return None

    def completedefault(self, *ignored):
        """Method called to complete an input line when no command-specific
        complete_*() method is available.
        """
        return []
