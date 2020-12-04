import sys
import ast
import contextlib
from os import remove
from io import StringIO

from userbot import bot
from userbot.commands import Command, register
from userbot.utils.mdtex import Section, SubSection, Bold, Code

@register
class Eval(Command):
    """Evaluate python code in the context of the bot"""

    command = "eval"
    category = "utils"

    async def exec(self, event):
        reply = await event.get_reply_message()
        if event.is_channel and not event.is_group:
            await event.edit("`Eval isn't permitted on channels`")
            return

        if event.pattern_match.group(1):
            expression = event.pattern_match.group(1).lstrip()
        elif reply:
            expression = reply.message.lstrip()
        else:
            await event.edit(str(Bold("Give an expression to evaluate")), delete_in=3)
            return

        head = Section(Bold("Query:"), Code(expression), indent=0)

        try:
            response, out = await self.async_eval(expression, bot=bot, event=event, reply=reply)
            evaluation = str(response)

            if evaluation:
                if isinstance(evaluation, str):
                    if len(evaluation) >= 4096:
                        file = open("output.txt", "w+")
                        file.write(evaluation)
                        file.close()
                        await bot.send_file(
                            event.chat_id,
                            "output.txt",
                            reply_to=event.id,
                            caption="`Output too large, sending as file`",
                        )
                        remove("output.txt")
                        return

            result = Section(Bold("Result:"), Code(response), indent=0)
            output = Section(Bold("Output:"), Code(out), indent=0)
            section = Section(
                head,
                result if response else None,
                output if out else None,
                indent=0,
                spacing=2
            )

            await event.edit(str(section))

        except Exception as err:
            error = SubSection(Bold("Error:"), Code(str(err)), indent=0)
            section = Section(head, error, indent=0, spacing=2)
            await event.edit(str(section))

    # https://stackoverflow.com/a/57349931/974936
    async def async_eval(self, code, **kwargs):
        # Note to self: please don't set globals here as they will be lost.
        # Don't clutter locals
        locs = {}
        # Restore globals later
        globs = globals().copy()
        # This code saves __name__ and __package into a kwarg passed to the function.
        # It is set before the users code runs to make sure relative imports work
        global_args = "_globs"
        while global_args in globs.keys():
            # Make sure there's no name collision, just keep prepending _s
            global_args = "_" + global_args
        kwargs[global_args] = {}
        for glob in ["__name__", "__package__"]:
            # Copy data to args we are sending
            kwargs[global_args][glob] = globs[glob]

        root = ast.parse(code, 'exec')
        code = root.body
        # If we can use it as a lambda return (but multiline)
        if isinstance(code[-1], ast.Expr):
            # Change it to a return statement
            code[-1] = ast.copy_location(ast.Return(code[-1].value), code[-1])
        # globals().update(**<global_args>)
        glob_copy = ast.Expr(ast.Call(func=ast.Attribute(value=ast.Call(func=ast.Name(id='globals', ctx=ast.Load()),
                                                                        args=[], keywords=[]),
                                                         attr='update', ctx=ast.Load()),
                                      args=[], keywords=[ast.keyword(arg=None,
                                                                     value=ast.Name(id=global_args, ctx=ast.Load()))]))
        glob_copy.lineno = 0
        glob_copy.col_offset = 0
        ast.fix_missing_locations(glob_copy)
        code.insert(0, glob_copy)
        args = []
        for a in list(map(lambda x: ast.arg(x, None), kwargs.keys())):
            a.lineno = 0
            a.col_offset = 0
            args += [a]
        fun = ast.AsyncFunctionDef('tmp', ast.arguments(
            args=[],
            vararg=None,
            kwonlyargs=args,
            posonlyargs=[],
            kwarg=None,
            defaults=[],
            kw_defaults=[None for i in range(len(args))]), code, [], None
        )
        fun.lineno = 0
        fun.col_offset = 0
        mod = ast.Module([fun], type_ignores=[])
        comp = compile(mod, '<string>', 'exec')

        exec(comp, {}, locs)

        with self.temp_stdio() as out:
            result = await locs["tmp"](**kwargs)
            try:
                globals().clear()
                # Inconsistent state
            finally:
                globals().update(**globs)
            return result, out.getvalue()

    @contextlib.contextmanager
    def temp_stdio(self, stdout=None, stderr=None):
        """Create a temporary STDIO for capturing results"""
        old_out = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old_out
