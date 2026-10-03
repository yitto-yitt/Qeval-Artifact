# EVAL_META: task_id=24, framework=qpanda, class=1

from pyqpanda3.core import *

def dj_algorithm(oracle):
    n = oracle.num_qubits
    init(QMachineType.CPU)
    try:
        qreg = qAlloc_many(n)
        prog = QProg()
        # Initial X on output qubit
        prog.insert(X(qreg[n - 1]))
        # First layer of Hadamards
        for i in range(n):
            prog.insert(H(qreg[i]))
        # Oracle application
        prog.insert(oracle)
        # Second layer of Hadamards
        for i in range(n):
            prog.insert(H(qreg[i]))
        # Simulate and obtain exact probabilities for input qubits
        qvm = QVM()
        qvm.init()
        input_qubits = [qreg[i] for i in range(n - 1)]
        prob_dict = qvm.probRunDict(prog, input_qubits)
        qvm.finalize()
        return prob_dict
    finally:
        finalize()
