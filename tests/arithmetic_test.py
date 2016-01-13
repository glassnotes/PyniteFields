import unittest
from pynitefields import * 

class ArithmeticTests(unittest.TestCase):
    def setUp(self):
        self.gf7= GaloisField(7)
        self.gf16= GaloisField(2, 4, [1, 1, 0, 0, 1])
        self.gf27= GaloisField(3, 3, [1, 2, 0, 1])


    def testAddition(self):
        # Adding 0
        self.assertEqual(self.gf7[2] + self.gf7[0], self.gf7[2])
        self.assertEqual(self.gf16[5] + self.gf16[0], self.gf16[5])
        self.assertEqual(self.gf27[3] + self.gf27[0], self.gf27[3])

        self.assertEqual(self.gf7[2] + self.gf7[3], self.gf7[5])
        #self.assertEqual(self.gf16[2] + self.gf16[3], self.gf16[])
        self.assertEqual(self.gf27[2] + self.gf27[3], self.gf27[11])


    def testSubtraction(self):
        self.assertEqual(self.gf7[2] - self.gf7[0], self.gf7[2])
        self.assertEqual(self.gf16[5] - self.gf16[0], self.gf16[5])
        self.assertEqual(self.gf27[3] - self.gf27[0], self.gf27[3])

        self.assertEqual(self.gf7[2] - self.gf7[3], self.gf7[6])
        #self.assertEqual(self.gf16[2] + self.gf16[3], self.gf16[])
        self.assertEqual(self.gf27[2] - self.gf27[3], self.gf27[18])


    def testMultiplication(self):
        self.assertEqual(self.gf7[2] * self.gf7[0], self.gf7[0])
        self.assertEqual(self.gf16[5] * self.gf16[0], self.gf16[0])
        self.assertEqual(self.gf27[3] * self.gf27[0], self.gf27[0])

        self.assertEqual(self.gf7[2] * self.gf7[3], self.gf7[6])
        self.assertEqual(self.gf16[2] * self.gf16[3], self.gf16[5])
        self.assertEqual(self.gf27[2] * self.gf27[3], self.gf27[5])

        # Test that it still works when you must wrap around
        self.assertEqual(self.gf16[4] * self.gf16[14], self.gf16[3])
        self.assertEqual(self.gf27[4] * self.gf27[24], self.gf27[2])


    def testDivision(self):
        self.assertEqual(self.gf7[2] / self.gf7[3], self.gf7[3])
        #self.assertEqual(self.gf16[2] + self.gf16[3], self.gf16[])
        self.assertEqual(self.gf27[2] / self.gf27[3], self.gf27[25])


    def testInverse(self):
        self.assertEqual(self.gf7[2].inv(), self.gf7[4])
        #self.assertEqual(self.gf16[2] + self.gf16[3], self.gf16[])
        self.assertEqual(self.gf27[16].inv(), self.gf27[10])


    def testPower(self):
        self.assertEqual(pow(self.gf7[0], 3), self.gf7[0])
        self.assertEqual(pow(self.gf16[0], 3), self.gf16[0])
        self.assertEqual(pow(self.gf27[0], 3), self.gf27[0])

        self.assertEqual(pow(self.gf7[2], 3), self.gf7[1])
        self.assertEqual(pow(self.gf16[2], 3), self.gf16[6])
        self.assertEqual(pow(self.gf16[9], 2), self.gf16[3])
        self.assertEqual(pow(self.gf27[8], 2), self.gf27[16])
        self.assertEqual(pow(self.gf27[14], 2), self.gf27[2])

    def testTrace(self):
        self.assertEqual(self.gf7[2].tr(), 2)
        #self.assertEqual(self.gf16[2] + self.gf16[3], self.gf16[])
        self.assertEqual(self.gf27[0].tr(), 0)
        self.assertEqual(self.gf27[11].tr(), 2)




if __name__ == '__main__':
    unittest.main()
