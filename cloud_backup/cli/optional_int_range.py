import click


class OptionalIntRange(click.IntRange):
    def convert(self, value, param, ctx):
        if value == '*' or value == 'None' or value == 'none' or value == 'N/A' or value == 'n/a':
            return None
        else:
            return super(OptionalIntRange, self).convert(value, param, ctx)
