

import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()

# ##Testing

# currTest = []
# portStatus1 = PortStatus(1,True)
# portStatus2 = PortStatus(3,True)
# portStatus3 = PortStatus(5,True)
# currTest.append(portStatus1)
# currTest.append(portStatus2)
# currTest.append(portStatus3)

# lastTest = []
# portStatus4 = PortStatus(3,True)
# portStatus5 = PortStatus(6,True)
# portStatus6 = PortStatus(10,True)
# lastTest.append(portStatus4)
# lastTest.append(portStatus5)
# lastTest.append(portStatus6)

# difference = self.compare(currTest, lastTest)
# ##Test