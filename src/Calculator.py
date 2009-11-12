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
        return self.evaluator(self.lnode.evaluate(), self.rnode.evaluate())

    def input(self, s):
        node_factory = NodeFactory()
        return node_factory.parseNode(s, self)

    def setLeftLeaf(self, node):
        self.lnode = node
        self.lnode.parent = self
    def setRightLeaf(self, node):
        self.rnode = node
        self.rnode.parent = self

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
    def __init__(self):
        self.operator_factory = OperatorFactory()
    def input(self, s):
        node = Node()
        return self.parseNode(s, node)
    def parseCompositeNode(self, s):
        composite = CompositeNode()
        composite.node = self.parseNode(s, Node())
        return composite
    def parseNode(self, s, node):
        s = s.strip()
        if 0 == len(s):
            return node
        op = self.operator_factory.findOperation(s)
        op_index = self.operator_factory.operatorIndex()
        
        if op is not None:
            node.evaluator = self.operator_factory.getOperation(op)
            node.operator_priority = self.operator_factory.getPriority(op)
            node.setLeftLeaf(self.parseLeftNode(s[:op_index]))
            self.parseRightNode(s[op_index+1 : ], node)
        else:
            node.setLeftLeaf(self.parseLeftNode(s))        
        return node
    def parseLeftNode(self, s):
        s = s.strip()
        if len(s)==0:
            return Leaf(0)
        if s[0]=="(":
            return self.parseCompositeNode(s[1:string.rfind(s, ')')])
        else:
            return Leaf(int(s))
    def parseRightNode(self, s, parent):
        node = Node()
        parent.setRightLeaf(node)
        self.parseNode(s, node)
        if self.isBranchSwapNecessary(parent):
            self.swapBranches(parent)       
        return node
    def isBranchSwapNecessary(self, node):
        if node.parent is None:
            return False
        if not self.isParentsOperatorHigherPriority(node):
            return False
        return True
    def isParentsOperatorHigherPriority(self, node):
        if node.parent.operator_priority > node.operator_priority:
            return True
        return False
    def swapBranches(self, node):
        self.swapEvaluator(node)
        self.swapParentsLeaves(node)
        self.exchangeRightLeafWithParent(node)
        self.swapLeaves(node)
    def swapEvaluator(self, node):
        if node.parent is not None:
            evaluator = node.evaluator
            node.evaluator = node.parent.evaluator
            node.parent.evaluator = evaluator
    def swapLeaves(self, node):
        n = node.rnode
        node.rnode = node.lnode
        node.lnode = n              
    def swapParentsLeaves(self, node):
        self.swapLeaves(node.parent)
    def exchangeRightLeafWithParent(self, node):
        p_rvalue = node.parent.rnode
        node.parent.setRightLeaf(node.rnode)
        node.setRightLeaf(p_rvalue)
