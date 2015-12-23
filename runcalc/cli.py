import click
import re


def time_str_to_seconds(s):
    if re.match('^\d+(\.\d+)?$', s):
        return float(s)
    if s.find(':') > 0:
        parts = [float(p) for p in s.split(':')]
        if len(parts) == 2:
            return 60 * parts[0] + parts[1]
        elif len(parts) == 3:
            return 60 * (60 * parts[0] + parts[1]) + parts[2]
    raise ValueError('Unknown time format: {}'.format(s))


def format_pace(pace, unit):
    minutes = int(pace // 60)
    seconds = pace % 60
    return '{}:{:.2f} minutes per {}'.format(
        minutes,
        seconds,
        unit
    )


class TimeType(click.ParamType):
    name = 'time'

    def convert(self, value, param, ctx):
        try:
            return time_str_to_seconds(value)
        except ValueError as e:
            self.fail(e, param, ctx)


TIME_PARAM = TimeType()


@click.command()
@click.option('--time', '-t', type=TIME_PARAM)
@click.option('--distance', '-d', type=float)
@click.option('--unit', '-u', default='mile')
def cli(time, distance, unit):
    """ Calculate running pace. """
    if not time:
        time = time_str_to_seconds(
            input('Enter the run time: ')
        )
    if not distance:
        distance = float(
            input('Enter the run distance: ')
        )
    pace = time / distance
    print('Pace:', format_pace(pace, unit))


if __name__ == '__main__':
    cli()
