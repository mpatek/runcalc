import datetime
import click
import re

_multipliers = {
    's': 1,
    'm': 60,
    'h': 3600,
}

_pattern = re.compile(
    '(?:(?:(?P<h>\d+):)?(?P<m>\d+):)?(?P<s>\d+(?:\.\d+)?)'
)


def time_str_to_seconds(s):
    """
    Convert a string representation of a time to number of seconds.

    Args:
        s (str): A string representation of a time.
    Returns:
        float: The number of seconds represented by the time string.

    Raises:
        ValueError: If the time string is in an unrecognized format.

    Examples:
        >>> time_str_to_seconds('123.45')
        123.45
        >>> time_str_to_seconds('7:15.45')
        435.45
        >>> time_str_to_seconds('1:07:15.45')
        4035.45
    """
    match = _pattern.match(s)
    if match:
        return sum(
            _multipliers[k] * float(v)
            for k, v in match.groupdict().items()
            if v and k in _multipliers
        )
    raise ValueError('Unknown time format: "{}"'.format(s))


def format_timedelta(td):
    """
    Format a timedelta

    Args:
        td (datetime.timedelta): A timedelta

    Returns:
        str: A string which represents the timedelta

    Examples:
        >>> import datetime
        >>> td = datetime.timedelta(days=3)
        >>> format_timedelta(td)
        '3 days'
        >>> td = datetime.timedelta(days=1)
        >>> format_timedelta(td)
        '1 day'
        >>> td = datetime.timedelta(seconds=14.2567)
        >>> format_timedelta(td)
        '14.26 seconds'
        >>> td = datetime.timedelta(seconds=64.6734)
        >>> format_timedelta(td)
        '1:04.67 minutes'
        >>> td = datetime.timedelta(seconds=3600)
        >>> format_timedelta(td)
        '1 hour'
        >>> td = datetime.timedelta(seconds=3673.123)
        >>> format_timedelta(td)
        '1 hour 1:13.12 minutes'
    """
    parts = []
    if td.days:
        parts.append('{} day{}'.format(td.days, 's' if td.days > 1 else ''))

    if td.seconds:

        hours = td.seconds // 3600

        if hours:
            parts.append('{} hour{}'.format(hours, 's' if hours > 1 else ''))
            minutes = (td.seconds % 3600) // 60
            seconds = (td.seconds % 3600) % 60
        else:
            minutes = td.seconds // 60
            seconds = td.seconds % 60

        if minutes:
            parts.append('{} minute{}'.format(
                minutes,
                's' if minutes > 1 else '',
            ))
        if seconds:
            hundredths = round(td.microseconds / 10000)
            f_hundredths = '.{}'.format(hundredths) if hundredths else ''
            parts.append('{}{} second{}'.format(
                seconds,
                f_hundredths,
                's' if seconds > 1 or f_hundredths else '',
            ))

    return ' '.join(parts)


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
    td = datetime.timedelta(seconds=pace)
    print('Pace:', format_timedelta(td), 'per', unit)


if __name__ == '__main__':
    cli()
