import re
import string
class Leaf(object):
    def __init__(self, value):
        self.value = value
        self.parent = None
    def evaluate(self):
        return self.value
class CompositeNode(object):
    def __init__(self):
        self.parent = None
        self.node = None
    def evaluate(self):
        return self.node.evaluate()

class Node(object):

    def __init__(self, lvalue=0, rvalue=0):
        '''
        Constructor
        '''
        self.setLeftLeaf(Leaf(lvalue))
        self.setRightLeaf(Leaf(rvalue))
        self.operators = OperatorFactory()
        self.evaluator = self.operators.getOperation('+')
        self.operator_priority = self.operators.getPriority('+')
        self.parent = None
    def evaluate(self):
        return self.evaluator(self.lvalue.evaluate(), self.rvalue.evaluate())

    def input(self, s):
        s = s.strip()
        if 0 == len(s):
            return
        op = self.operators.findOperation(s)
        op_index = self.operators.operatorIndex()
        
        node_factory = NodeFactory()
        if op is not None:
            self.evaluator = self.operators.getOperation(op)
            self.operator_priority = self.operators.getPriority(op)
            self.setLeftLeaf(node_factory.input(s[:op_index]))
            node_factory.parseNode(s[op_index+1 : ], self)
            if self.isBranchSwapNecessary():
                self.swapBranches()
        else:
            self.setLeftLeaf(node_factory.input(s))


    def setLeftLeaf(self, node):
        self.lvalue = node
        self.lvalue.parent = self
    def setRightLeaf(self, node):
        self.rvalue = node
        self.rvalue.parent = self

    def swapBranches(self):
        self.swapEvaluator()
        self.swapParentsLeaves()
        self.exchangeRightLeafWithParent()
        self.swapLeaves()
    def isBranchSwapNecessary(self):
        if self.parent is None:
            return False
        if self.parent.operator_priority <= self.operator_priority:
            return False
        return True        
    def swapEvaluator(self):
        if self.parent is not None:
            evaluator = self.evaluator
            self.evaluator = self.parent.evaluator
            self.parent.evaluator = evaluator
    def swapParentsLeaves(self):
        self.parent.swapLeaves()
    def swapLeaves(self):
        node = self.rvalue
        self.rvalue = self.lvalue
        self.lvalue = node            
    def exchangeRightLeafWithParent(self):
        p_rvalue = self.parent.rvalue
        self.parent.setRightLeaf(self.rvalue)
        self.setRightLeaf(p_rvalue)

                  
class OperatorFactory(object):
    def __init__(self):
        self.index = None
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
        stack = 0
        for i in range(len(s)):
            if s[i] == "(":
                stack +=1
            elif s[i] == ")":
                stack -=1
            else:
                match = re.search("[-+\*\/]", s[i])
                if hasattr(match, 'group') and stack==0:
                    self.index = i
                    return match.group(0)
        
    def operatorIndex(self):
        return self.index
    def getPriority(self, op):
        if op == "+":
            return 1
        elif op == "-":
            return 2
        return 3
class NodeFactory(object):
    def input(self, s):
        s = s.strip()
        if len(s)==0:
            return Leaf(0)
        if s[0]=="(":
            return self.parseCompositeNode(s[1:string.rfind(s, ')')])
        else:
            return Leaf(int(s))
    def parseCompositeNode(self, s):
        node = CompositeNode()
        calc = Node()
        calc.operators = OperatorFactory()
        calc.input(s)
        node.node = calc
        return node
    def parseNode(self, s, parent):
        node = Node()
        parent.setRightLeaf(node)
        node.input(s)
        return node