
import unittest
import Calculator
class NodeProxy(Calculator.Node):
    def __init__(self, factory, node):
        Calculator.Node.__init__(self)
        self.factory = factory
        self.node = node
        self.parent = None
        self.node.operators = Calculator.OperatorFactory()
        self.lnode = self.node.lnode
        self.rnode = self.node.rnode
    def fix(self):
        self.lnode = self.node.lnode
        self.rnode = self.node.rnode
    def evaluate(self):
        return self.node.evaluate()
    def input(self, s):
        self.node = self.factory.input(s)
        self.fix()
        return self.node
class CalculatorTest(unittest.TestCase):


    def setUp(self):
        self.sut = NodeProxy(Calculator.NodeFactory(), Calculator.Node())

    def tearDown(self):
        del self.sut

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
        lnode = self.sut.lnode
        sut = sut.node
        self.assertEquals(sut, lnode.parent)
    def testOperationShouldImposeParentChildRelationship(self):
        sut = self.sut
        sut = sut.input("2*5")
        lnode = sut.lnode
        self.assertEquals(sut, lnode.parent)
    def testOperationOnMultiDigit(self):
        sut = self.sut
        sut.input("20*5")
        self.assertEquals(100, sut.evaluate())        
    def testEvenleavesOfTheSimplestExpressionShouldHaveParentInitialized(self):
        sut = self.sut
        sut.input("5")
        lnode = sut.lnode
        sut = sut.node
        self.assertEquals(sut, lnode.parent)
    def testRightSideOfTheExpressionShouldAlsoHaveParentInitialized(self):
        sut = self.sut
        sut = sut.input("5+5")
        rnode = sut.rnode
        self.assertEquals(sut, rnode.parent)
    def testCalulatorShouldBeAbleToSwapItsLeaves(self):
        sut = self.sut
        sut.setLeftLeaf(Calculator.Leaf(3))
        sut.setRightLeaf(Calculator.Leaf(2))
        factory = Calculator.NodeFactory()
        factory.swapLeaves(sut)
        self.assertEquals(3, sut.rnode.evaluate())
        self.assertEquals(2, sut.lnode.evaluate())

        
        

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
    def testCanEvaluateCompoundExpressionEvenIfParanthesisAreTheFirstMultiplicationVersion(self):
        sut = self.sut
        sut.input("(2-1)*3")
        self.assertEqual(3, sut.evaluate())
    def testCanEvaluateVeryCompoundExpressionsEvenIfParanthesisAreInvolved(self):
        sut = self.sut
        sut.input("((2-1)*2)-2")
        self.assertEqual(0, sut.evaluate())
    def testCanEvaluateTwoMultiplicationsSeparatedByAdditions(self):
        sut = self.sut
        sut.input("2*3+2+3+3*2")
        self.assertEqual(17, sut.evaluate())
    def testSingleExpressionInParanthesisShouldBecomeLeftNode(self):
        self.sut.input("(2+3)")
        self.assertEqual(0, self.sut.rnode.evaluate())
    
class OperatorFactoryTest(unittest.TestCase):
    def setUp(self):
        self.sut = Calculator.OperatorFactory()
    def tearDown(self):
        del self.sut
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
    def testReturnedIndexShouldBeNoneIfOperatorNotFound(self):
        self.sut.findOperation('0123')
        self.assertEquals(None, self.sut.operatorIndex())
    def testShouldIgnoreParanthesisWhenSearchingForOperator(self):
        self.assertEqual("+", self.sut.findOperation("(2-2)+10"))
    def testShouldFindOperatorBetweenTwoBraces(self):
        self.assertEqual("+", self.sut.findOperation("((2-2)*2)+(2-2)"))
    def testShouldIndicatePositionOfOperatorFound(self):
        self.sut.findOperation("((2-2)*2)+(2-2)")
        self.assertEqual(9,self.sut.operatorIndex())
    def testShouldNotFindAnyOperator(self):
        self.assertTrue(self.sut.findOperation("(2+2)") is None)
    def testAdditionShouldHaveLowestPriority(self):
        self.assertEqual(1,self.sut.getPriority('+'))
    def testSubstractionBindBitTighter(self):
        self.assertEqual(2,self.sut.getPriority('-'))
    def testMultiplicationHaveHigherPriorityThanAddition(self):
        self.assertTrue(self.sut.getPriority("+") < self.sut.getPriority("*"))
    def testSubstractionHasTheSamePriorityAsAddition(self):
        self.assertTrue(self.sut.getPriority("+") < self.sut.getPriority("-"))
        
class NodeFactoryTest(unittest.TestCase):
    def setUp(self):
        self.sut = Calculator.NodeFactory()
    def tearDown(self):
        pass
    def testNodeFactoryShouldCreateNodeFromString(self):
        self.assertTrue(hasattr(self.sut.input(""), 'evaluate'))
    def testSimpleNodeShouldHaveTheValueParsed(self):
        node = self.sut.input("5")
        self.assertEqual(5, node.evaluate())
    def testSimpleNodeInBracketsShouldBeParsed(self):
        node = self.sut.input(" (5)")
        self.assertTrue(5, node.evaluate())
    def testShouldBeAbleToSwapOperationsWithItsParent(self):
        sut = self.sut
        sut = sut.input("3+2-2")
        rvalue = sut.rnode
        self.sut.swapEvaluator(rvalue)
        self.assertEqual(0,sut.evaluator(2,2))        
    def testShouldNotSwapEvaluatorIfRootNode(self):
        sut = self.sut
        node = sut.input("3+2")
        self.sut.swapEvaluator(node)
        self.assertEqual(4, node.evaluator(2,2))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testShouldParseInput']
    unittest.main()