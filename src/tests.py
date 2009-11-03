
import unittest
import Calculator

class CalculatorTest(unittest.TestCase):


    def setUp(self):
        self.sut = Calculator.Calculator()
        self.sut.operators = Calculator.OperatorFactory()

    def tearDown(self):
        pass

    def testShouldParseInput(self):
        sut = self.sut
        sut.input("")
    def testShouldEvaluteToZeroByDefault(self):
        sut = self.sut
        self.assertEqual(0,sut.evaluate())
    def testShouldParseSimpleExpressionAndEvaluate(self):
        sut = self.sut
        sut.input("5+5")
        self.assertEqual(10, sut.evaluate())
    def testShouldParseSingleDigitAndEvaluateIt(self):
        sut = self.sut
        sut.input("5")
        self.assertEqual(5, sut.evaluate())
    def testShouldUnderstandThatOperationCanBeWrittenInFrontOfADigit(self):
        sut = self.sut
        sut.input("+5")
        self.assertEqual(5, sut.evaluate())
    def testSimpleExpressionCanHaveOperationInFrontOfFirstDigit(self):
        sut = self.sut
        sut.input("+5+5")
        self.assertEqual(10, sut.evaluate())
    def testCalculatorShouldBeAbleToComputeResultsWithMoreThanOneNode(self):
        sut = self.sut
        sut.input("5+10+15")
        self.assertEqual(30, sut.evaluate())
    def testCalculatorShouldBeAbleToComputeEvenQuiteLongExpressions(self):
        sut = self.sut
        sut.input("5+10+15+20+30+20")
        self.assertEqual(100, sut.evaluate())
    def testWhiteSpaceShouldBeInsignificant(self):
        sut = self.sut
        sut.input(" + 5+10+ 15")
        self.assertEqual(30, sut.evaluate())
    def testShouldBeAbleToSubstract(self):
        sut = self.sut
        sut.input ("5-5")
        self.assertEqual(0, sut.evaluate())
    def testShouldBeAbleToSubstractCorrectly(self):
        sut = self.sut
        sut.input("2-3+4")
        self.assertEqual(3, sut.evaluate())
    
    def testShouldBeAbleToMultiply(self):
        sut = self.sut
        sut.input("2*5")
        self.assertEqual(10, sut.evaluate())
    def testShouldBeAbleToSubstractAndMultiply(self):
        sut = self.sut
        sut.input("2*5-5")
        self.assertEqual(5, sut.evaluate())        
    def testShouldConsiderMultiplicationOfHigherPriority(self):
        sut = self.sut
        sut.input("2+5*5")
        self.assertEqual(27, sut.evaluate())
    def testShouldConsiderMultiplicationOfHigherPriority_test2(self):
        sut = self.sut
        sut.input("2*5+5")
        self.assertEqual(15, sut.evaluate())
    def testRootShouldNotHaveParent(self):
        sut = self.sut
        self.assertTrue(sut.parent is None)
    def testLeavesShouldHaveParentFieldInitialized(self):
        sut = self.sut
        lnode = self.sut.lvalue
        self.assertEquals(sut, lnode.parent)
    def testOperationShouldImposeParentChildRelationship(self):
        sut = self.sut
        sut.input("2*5")
        lnode = sut.lvalue
        self.assertEquals(sut, lnode.parent)
    def testOperationOnMultiDigit(self):
        sut = self.sut
        sut.input("20*5")
        self.assertEquals(100, sut.evaluate())        
    def testEvenleavesOfTheSimplestExpressionShouldHaveParentInitialized(self):
        sut = self.sut
        sut.input("5")
        lnode = sut.lvalue
        self.assertEquals(sut, lnode.parent)
    def testRightSideOfTheExpressionShouldAlsoHaveParentInitialized(self):
        sut = self.sut
        sut.input("5+5")
        rnode = sut.rvalue
        self.assertEquals(sut, rnode.parent)
    def testCalulatorShouldBeAbleToSwapItsLeaves(self):
        sut = self.sut
        sut.setLeftLeaf(Calculator.Node(3))
        sut.setRightLeaf(Calculator.Node(2))
        sut.swapLeaves()
        self.assertEquals(3, sut.rvalue.evaluate())
        self.assertEquals(2, sut.lvalue.evaluate())
    def testShouldBeAbleToSwapOperationsWithItsParent(self):
        sut = self.sut
        sut.input("3+2-2")
        rvalue = sut.rvalue
        rvalue.swapEvaluator()
        self.assertEqual(4,sut.evaluator(2,2))
        
        
    def testShouldNotSwapEvaluatorIfRootNode(self):
        sut = self.sut
        sut.input("3+2")
        sut.swapEvaluator()
        self.assertEqual(4, sut.evaluator(2,2))
    def testShouldBeableToComputeDivision(self):
        sut = self.sut
        sut.input("2/2")
        self.assertEqual(1, sut.evaluate())
    def testDivisionAndSubstractionAreSensitiveToPosition(self):
        sut = self.sut
        sut.input("2/2-1")
        self.assertEqual(0, sut.evaluate())
    def testCanEvaluateNegativeExpressions(self):
        sut = self.sut
        sut.input("-1")
        self.assertEqual(-1, sut.evaluate())
    def testParsingEmptyStringShouldCreateZeroNode(self):
        sut = Calculator.Node.input("")
        self.assertEqual(0, sut.evaluate())
    def testCanEvaluateExpressionsInParanthesis(self):
        sut = self.sut
        sut.input("(2+2)")
        self.assertEqual(4, sut.evaluate())
    def testCanEvaluateDoubleParanthesis(self):
        sut = self.sut
        sut.input("((2) )")
        self.assertEqual(2, sut.evaluate())
    def testCanEvaluateCompoundExpressions(self):
        sut = self.sut
        sut.input("(2+(2-2))")
        self.assertEqual(2, sut.evaluate())
    def testCanEvaluateCompoundExpressionEvenIfParanthesisAreTheFirst(self):
        sut = self.sut
        sut.input("(2-1)+3")
        self.assertEqual(4, sut.evaluate())
    def testCanEvaluateVeryCompoundExpressionsEvenIfParanthesisAreInvolved(self):
        sut = self.sut
        sut.input("((2-1)*2)-2")
        self.assertEqual(-1, sut.evaluate())
    
class OperatorFactoryTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testPlusShouldStandForAddition(self):
        sut = Calculator.OperatorFactory()
        func = sut.getOperation('+')
        self.assertEquals(10, func(5,5))
    def testFactoryShouldRecognizeTheFirstOperation(self):
        sut = Calculator.OperatorFactory()
        func = sut.getOperation('5+5')
        self.assertEquals(10, func(5,5))
    def testShouldReturnNoneIfOperationNotFound(self):
        sut = Calculator.OperatorFactory()
        op = sut.findOperation('')
        self.assertTrue(op is None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testShouldParseInput']
    unittest.main()