from logging import Logger, getLogger, basicConfig
import click

from bobday_app import App, ApplicationError, DEFAULT_LOGGER_FORMAT

logger: Logger = getLogger("Application logger")


@click.command
@click.argument('username')
@click.argument('password')
@click.option('--debug', default=False, help='Log level')
def cli(username: str, password: str, debug: bool):
    try:
        basicConfig(level='DEBUG' if debug else 'INFO', **DEFAULT_LOGGER_FORMAT)  # type: ignore
        App(username, password).get().group_by_department().save_to_file().post()
    except (KeyboardInterrupt, ApplicationError) as ex:
        logger.error(str(ex))
