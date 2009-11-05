import re
import string
class Node(object):
    def __init__(self, value):
        self.value = value
        self.parent = None
    def evaluate(self):
        return self.value
    @staticmethod
    def input(s):
        if len(s)==0:
            return Node(0)
        else:
            return Node(int(s))
class CompositeNode(object):
    def __init__(self):
        self.value = 0
        self.parent = None
        self.node = None
    def evaluate(self):
        return self.node.evaluate()
class OperatorFactory(object):
    def __init__(self):
        pass
    def getOperation(self, s):
        mnemonic = self.findOperation(s)
        if mnemonic == '+':
            return lambda l, r: l+r
        elif mnemonic == '-':
            return lambda l, r: l-r
        elif mnemonic == '*':
            return lambda l, r: l*r
        elif mnemonic == '/':
            return lambda l, r: l/r
    def findOperation(self, s):
        match = re.search("[-+\*\/]", s)
        if (hasattr(match, 'group')):
            return match.group(0)
    def getPriority(self, op):
        if op == "+":
            return 1
        elif op == "-":
            return 2
        return 3
class Calculator(object):

    def __init__(self, lvalue=0, rvalue=0):
        '''
        Constructor
        '''
        self.setLeftLeaf(Node(lvalue))
        self.setRightLeaf(Node(rvalue))

        self.evaluator = lambda left,right: left  + right
        self.parent = None

    def input(self, s):
        s = s.strip()
        if 0 == len(s):
            return
        last = 0
        if s[0]=="(":
            last = string.rfind(s,")")
            return self.input(s[0+1:last] + s[last+1:])
        op = self.operators.findOperation(s)
        
        if op is not None:
            self.evaluator = self.operators.getOperation(op)
            self.operator_priority = self.operators.getPriority(op)
            self.setLeftLeaf(Node.input(s[last : s.index(op)]))
            self.createCalcNode(s[s.index(op) + 1:])

            if self.parent is not None:
                self.swapBranches()
        else:
            self.setLeftLeaf(Node.input(s))

    def evaluate(self):
        return self.evaluator(self.lvalue.evaluate(), self.rvalue.evaluate())
    def swapLeaves(self):
        node = self.rvalue
        self.rvalue = self.lvalue
        self.lvalue = node
    def swapEvaluator(self):
        if self.parent is not None:
            evaluator = self.evaluator
            self.evaluator = self.parent.evaluator
            self.parent.evaluator = evaluator
    def setLeftLeaf(self, node):
        self.lvalue = node
        self.lvalue.parent = self
    def setRightLeaf(self, node):
        self.rvalue = node
        self.rvalue.parent = self

    def createCalcNode(self, s):
        rvalue = Calculator()
        rvalue.operators = self.operators
        self.setRightLeaf(rvalue)
        rvalue.input(s)
        return rvalue

    def swapBranches(self):
        if self.parent.operator_priority <= self.operator_priority:
            return
        self.swapEvaluator()
        self.parent.swapLeaves()
        p_rvalue = self.parent.rvalue
        self.parent.setRightLeaf(self.rvalue)
        self.setRightLeaf(p_rvalue)
        self.swapLeaves()

