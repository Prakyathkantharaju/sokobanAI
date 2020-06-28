# This class is to store the state and weight for A-star search

class queue(object):
    def __init__(self,len_state):
        # len_state is the len of the box + worker
        self.data = {}
