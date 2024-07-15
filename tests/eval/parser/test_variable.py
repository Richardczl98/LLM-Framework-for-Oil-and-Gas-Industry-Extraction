import unittest

from schema.variables import get_variable


class TestVariable(unittest.TestCase):
    def setUp(self) -> None:
        print('\n')

    def test_get_variables_by_section(self):
        section = 'Production methods'
        got = get_variable(section)
        want = [
            'name: Downhole pump, section: Production methods, unit: , prompt: ',
            'name: Water reinjection, section: Production methods, unit: , prompt: ',
            'name: Natural gas reinjection, section: Production methods, unit: , prompt: ',
            'name: Water flooding, section: Production methods, unit: , prompt: ',
            'name: Gas lifting, section: Production methods, unit: , prompt: ',
            'name: Gas flooding, section: Production methods, unit: , prompt: ',
            'name: Steam flooding, section: Production methods, unit: , prompt: ',
            'name: Oil sands mine (integrated with upgrader), section: Production methods, unit: , prompt: ',
            'name: Oil sands mine (non-integrated with upgrader), section: Production methods, unit: , prompt: ',
            ]

        for var, want_text in zip(got, want):
            assert str(var) == want_text

    def test_get_variables_by_name(self):
        var_names = ['Downhole pump', 'Water reinjection', 'Natural gas reinjection', 'Water flooding',
                     'Gas lifting', 'Gas flooding', 'Steam flooding']
        got = get_variable(var_names=var_names)
        want = [
            'name: Downhole pump, section: Production methods, unit: , prompt: ',
            'name: Water reinjection, section: Production methods, unit: , prompt: ',
            'name: Natural gas reinjection, section: Production methods, unit: , prompt: ',
            'name: Water flooding, section: Production methods, unit: , prompt: ',
            'name: Gas lifting, section: Production methods, unit: , prompt: ',
            'name: Gas flooding, section: Production methods, unit: , prompt: ',
            'name: Steam flooding, section: Production methods, unit: , prompt: ',
            ]

        for var, want_text in zip(got, want):
            assert str(var) == want_text
