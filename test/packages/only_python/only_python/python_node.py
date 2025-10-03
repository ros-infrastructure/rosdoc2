import dummy_module
import test_of_automock

test_of_automock.hello()
dummy_module.goodbye()


def main():
    print('Hi from only_python.')


class DummyClass:
    """A dummy class for testing purposes."""

    def __init__(self):
        self.value = 42

    def get_value(self):
        return self.value


if __name__ == '__main__':
    main()
