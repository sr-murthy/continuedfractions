from __future__ import annotations


__all__ = [
    'NamedCallableProxy',
]


# -- IMPORTS --

# -- Standard libraries --
from typing import Any, Callable

# -- 3rd party libraries --

# -- Internal libraries --


class NamedCallableProxy:
    """Class wrapper to have named callable proxies, which can also work as :py:class:`enum.Enum` values.

    Adapted from Stack Overflow solution by Ceppo93:

        https://stackoverflow.com/a/40486992
    """
    __slots__ = ('_callable', '_name')

    _callable: Callable
    _name: str

    def __new__(cls, callable_: Callable, /, *, name: str = None) -> NamedCallableProxy:
        """Constructor

        Parameters
        ----------
        callable_ : `callable`
            The callable to name and proxy.

        name : `str`, default=None
            The user-defined name of the callable to use in :py:func:`~continuedfractions.utils.__repr__`.
            If :py:data:`None` the Python-defined default will be used.

        Returns
        -------
        callable
            A named callable proxy.

        Examples
        --------
        >>> square = NamedCallableProxy(lambda x: x ** 2, name="square: x |--> x^2")
        >>> square
        NamedCallableProxy("square: x |--> x^2")
        >>> list(map(square, [1, 2, 3, 4, 5]))
        [1, 4, 9, 16, 25]
        """
        self = super().__new__(cls)
        self._callable = callable_
        self._name = name

        return self

    def __repr__(self) -> str:
        if self._name:
            return f'{self.__class__.__name__}("{self._name}")'

        return str(self._callable)

    def __eq__(self, other: NamedCallableProxy) -> bool:
        return self._callable.__code__.co_code == other._callable.__code__.co_code

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._callable(*args, **kwargs)


if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     python -m doctest -v src/continuedfractions/utils.py
    #
    import doctest
    doctest.testmod()
