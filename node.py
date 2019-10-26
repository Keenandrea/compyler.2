import token

class Node(object):
    def __init__(self, label = "", depth = 0, child1 = None, child2 = None, child3 = None, child4 = None, token1 = token.Token(), token2 = token.Token()):
        self._label = label
        self._depth = depth
        self._child1 = child1
        self._child2 = child2
        self._child3 = child3
        self._child4 = child4
        self._token1 = token1
        self._token2 = token2

    # def push_back(self, tok):
    #     self.token1.append(tok)  
 
    @property
    def label(self):
        return self._label

    @property
    def depth(self):
        return self._depth  

    @property
    def child1(self):
        return self._child1

    @property
    def child2(self):
        return self._child2

    @property
    def child3(self):
        return self._child3

    @property
    def child4(self):
        return self._child4

    @property
    def token1(self):
        return self._token1

    @property
    def token2(self):
        return self._token2

    @label.setter
    def label(self, lbl):
        self._label = lbl

    @depth.setter
    def depth(self, dth):
        self._depth = dth

    @child1.setter
    def child1(self, ch1):
        self._child1 = ch1

    @child2.setter
    def child2(self, ch2):
        self._child2 = ch2

    @child3.setter
    def child3(self, ch3):
        self._child3 = ch3

    @child4.setter
    def child4(self, ch4):
        self._child4 = ch4

    @token1.setter
    def token1(self, tok):
        self._token1 = tok

    @token2.setter
    def token2(self, tok):
        self._token2 = tok

    # class Node(object):
    # def __init__(self, label = "", depth = 0):
    #     self.label = label
    #     self.depth = depth
    #     self.children = []
    #     self.tokenize = []

    # def push_back_child(self, child):
    #     self.children.append(child) 

    # def push_back_token(self, tok):
    #     self.tokenize.append(tok) 