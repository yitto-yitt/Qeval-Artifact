# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, X, measure

def xor_gate(a, b):
    n = 8
    xor_val = a ^ b
    qvm = CPUQVM()
    circuit = QCircuit()
    for i in range(n):
        if (xor_val >> i) & 1:
            circuit << X(i)
    prog = QProg()
    prog << circuit
    for i in range(n):
        prog << measure(i, i)
    qvm.run(prog, 1000)
    result = qvm.result().get_counts()
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
