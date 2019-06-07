class alphaBeta:
    def __init__(self, tree):
        self.tree = tree
        self.root = tree.root
        return
    def search(self, node):
        infinity = float('inf')
        best = -infinity
        beta = infinity
        # successor = legal moves
        legalMoves = self.legalMoves(node)
        bestState = None
        for state in legalMoves:
            value = self.minVal(state, best, beta)
            if val > best:
                best = val
                bestState = state
        return bestState
    def maxValue(self, node, alpha, beta):
        if self.terminal(node):
            return self.utility(node)
        infinity = float('inf')
        val = -infinity
        legalMoves = self.legalMoves(node)
        for state in legalMoves:
            val = max(val, self.minVal(state, alpha, beta))
            if val >= beta:
                return val
            alpha = max(alpha, val)
                return val

