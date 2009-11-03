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
        if s[0]=="(":
            last = string.rfind(s,")")
            return self.input(s[0+1:last] + s[last+1:])
        op = self.operators.findOperation(s)
        
        if op is not None:
            self.evaluator = self.operators.getOperation(op)
            self.setLeftLeaf(Node.input(s[ : s.index(op)]))
            self.createCalcNode(s[s.index(op) + 1:])

            if self.parent is not None and op in ['+', '-']:
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
        self.swapEvaluator()
        self.parent.swapLeaves()
        p_rvalue = self.parent.rvalue
        self.parent.setRightLeaf(self.rvalue)
        self.setRightLeaf(p_rvalue)
        self.swapLeaves()

