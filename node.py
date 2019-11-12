import token
from collections import deque

class Node(object):
    def __init__(self, label = "", depth = None, child1 = None, child2 = None, child3 = None, child4 = None, token1 = token.Token(), token2 = token.Token(), token3 = token.Token(), token4 = token.Token()):
        self.label = label
        self.depth = depth
        self.child1 = child1
        self.child2 = child2
        self.child3 = child3
        self.child4 = child4
        self.token1 = token1
        self.token2 = token2
        self.token3 = token3
        self.token4 = token4
        self.child_list = [] 
        self.token_list = [] 

    # def push_child1(self, child1):
    #     self.child_list.append(child1)

    # def push_token(self, tok):
    #     self._token_list.append(tok)

 
    # @property
    # def label(self):
    #     return self._label

    # @property
    # def depth(self):
    #     return self._depth  

    # @property
    # def child1(self):
    #     return self._child1

    # @property
    # def child2(self):
    #     return self._child2

    # @property
    # def child3(self):
    #     return self._child3

    # @property
    # def child4(self):
    #     return self._child4

    # @property
    # def token1(self):
    #     return self._token1

    # @property
    # def token2(self):
    #     return self._token2

    # @label.setter
    # def label(self, lbl):
    #     self._label = lbl

    # @depth.setter
    # def depth(self, dth):
    #     self._depth = dth

    # @child1.setter
    # def child1(self, ch1):
    #     self._child1 = ch1

    # @child2.setter
    # def child2(self, ch2):
    #     self._child2 = ch2

    # @child3.setter
    # def child3(self, ch3):
    #     self._child3 = ch3

    # @child4.setter
    # def child4(self, ch4):
    #     self._child4 = ch4

    # @token1.setter
    # def token1(self, tok):
    #     self._token1 = tok

    # @token2.setter
    # def token2(self, tok):
    #     self._token2 = tok