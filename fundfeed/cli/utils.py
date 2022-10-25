import click
import time
from eth_utils import encode_hex
from eth_abi import encode_abi


class RequiredIf(click.Option):
    def __init__(self, *args, **kwargs):
        self.required_if = kwargs.pop('required_if')
        assert self.required_if, "'required_if' parameter required"
        kwargs['help'] = (kwargs.get('help', '') +
            ' NOTE: This argument is mutually exclusive with %s' %
            self.required_if
        ).strip()
        super(RequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        flag_present = self.name in opts
        requirement_present = self.required_if in opts
        
        if not requirement_present and self.required_if != 'fund_only':
            raise click.UsageError(
                "Choose either --fund-only(feed id required) flag or --setup-datafeed flag"
            )

        if not requirement_present or not opts['setup_datafeed']:
            self.prompt = None
        else:
            if self.name == 'start_time':
                click.echo(click.style(f"Current time: {int(time.time())}", fg=126))
            self.prompt = click.style(self.name.capitalize().replace("_", " "), fg=126)

        if self.required_if == 'fund_only' and not opts['setup_datafeed']:
            self.prompt = "Feed id"
        if not requirement_present and flag_present:
            requirement = self.required_if.replace("_", "-")
            raise click.UsageError(
                    f"Please use flag --{requirement}"
                )

        return super(RequiredIf, self).handle_parse_result(
            ctx, opts, args)

def build_query_data():
    query_type = colored_prompt("Enter query type", str)
    param_types = colored_prompt("Enter parameter types separated by space", str.split)
    params = colored_prompt("Enter parameters separated by space", str.split)

    for param_typ in param_types:
        if param_typ.startswith('uint'):
            index = param_types.index(param_typ)
            params[index] = int(params[index])
    paramaters = encode_abi(param_types, params)
    return encode_hex(encode_abi(["string", "bytes"], [query_type, paramaters]))

def colored_style(text):
    return click.style(text, fg=[69, 222, 187])

def colored_prompt(text, type):
    return click.prompt(colored_style(text), type=type)
