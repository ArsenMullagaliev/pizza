from typing import Callable
import click
from random import randint


class Pizza:
    """Defines Pizza objects."""

    SIZES = ['L', 'XL']
    SIZES_FULL_NAME = {'L': 'Large', 'XL': 'Extra Large'}
    DELIVERY_REQUIRED_TEXT_STATUS = {True: 'with', False: 'without'}

    def __init__(self, ingredients: list[str], size: str = 'L'):
        if size not in self.SIZES:
            raise ValueError('Invalid pizza size!')
        self._size = size
        self.ingredients = ingredients

    def dict(self) -> dict[str, str]:
        return {'ingredients': f'{", ".join([ingredient for ingredient in self.ingredients])}',
                'size': self.size}

    def __eq__(self, other: object) -> bool:
        """Compares Pizzas by recipe name and size."""
        if not isinstance(other, Pizza):
            return NotImplemented
        return (self.size == other.size) & (self.__class__.__name__ == other.__class__.__name__)

    def __str__(self) -> str:
        """Returns Pizza name and ingredient list."""
        return f'{self.__class__.__name__}: \
{", ".join([ingredient for ingredient in self.ingredients])}.'

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        if new_size not in self.SIZES:
            raise ValueError(f'Only these sizes available: {self.SIZES}')
        self._size = new_size


class EmojiMixin:
    """Adds emoji to Pizza __str__ method."""

    EMOJI_DICT = {
        'Margherita': '🧀',
        'Pepperoni': '🍕',
        'Hawaiian': '🍍'
    }

    def __str__(self) -> str:
        return f'{self.__class__.__name__} \
{self.EMOJI_DICT[self.__class__.__name__]}: \
{", ".join([ingredient for ingredient in self.ingredients])}.'


class Pepperoni(EmojiMixin, Pizza):
    """Defines Pepperoni Pizza"""

    INGREDIENTS = ['tomato sauce', 'mozzarella', 'pepperoni']

    def __init__(self, size: str = 'L'):
        super().__init__(size=size, ingredients=self.INGREDIENTS)


class Margherita(EmojiMixin, Pizza):
    """Defines Pizza Margherita"""

    INGREDIENTS = ['tomato sauce', 'mozzarella', 'tomatoes']

    def __init__(self, size: str = 'L'):
        super().__init__(size=size, ingredients=self.INGREDIENTS)


class Hawaiian(EmojiMixin, Pizza):
    """Defines Hawaiian Pizza"""

    INGREDIENTS = ['tomato sauce', 'mozzarella', 'chicken', 'pineapples']

    def __init__(self, size: str = 'L'):
        super().__init__(size=size, ingredients=self.INGREDIENTS)


def track_time(template: str):
    """Prints time it took to execute function.
    Takes template and adds time in seconds using formatted string"""
    def wrapper(func: Callable):
        def decorated(*args, **kwargs):
            execution_time = randint(0, 10)
            print(template.format(execution_time))
            return func(*args, **kwargs)
        return decorated
    return wrapper


@track_time('Baked in {} min')
def bake() -> None:
    """Готовит пиццу"""
    return None


@track_time('Delivered in {} min')
def deliver() -> None:
    """Доставляет пиццу"""
    return None


@track_time('Picked up in {} min')
def pickup() -> None:
    """Выдает пиццу"""
    return None


@click.group()
def cli() -> None:
    """Initiates click interface"""
    return None


@cli.command()
@click.option(
    '--pizza',
    type=click.Choice(
        [pizza_subclass.__name__ for pizza_subclass in Pizza.__subclasses__()],
        case_sensitive=False),
    prompt='What kind of pizza?',
    help='Run menu command for options.')
@click.option(
    '--size',
    type=click.Choice(Pizza.SIZES,  case_sensitive=False),
    prompt='What size?',
    help='We have L and XL pizzas')
@click.option('--delivery', prompt='Delivery needed?', default=False, is_flag=True)
def order(pizza: str, delivery: bool, size: str) -> None:
    """Готовит и доставляет пиццу"""
    pizza_name = pizza.capitalize()
    pizza_ordered = globals()[pizza_name]()
    pizza_size = pizza_ordered.SIZES_FULL_NAME[size.upper()]
    with_or_without_string = pizza_ordered.DELIVERY_REQUIRED_TEXT_STATUS[delivery]
    message = f'{pizza_size} {pizza_name} {with_or_without_string} delivery ordered!'
    print()  # Add empty line to move text from the menu
    print(message)
    bake()
    if delivery:
        deliver()
    else:
        pickup()
    return None


@cli.command()
def menu():
    """Выводит меню"""
    for pizza_subclass in Pizza.__subclasses__():
        print(f'- {pizza_subclass()}')


if __name__ == '__main__':
    cli()
