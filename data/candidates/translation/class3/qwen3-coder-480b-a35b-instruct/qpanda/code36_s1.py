# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda import *

def bv_function(s):
    n = len(s)
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n + 1)
    cbits = qvm.cAlloc_many(n + 1)
    prog = QProg()
    circuit = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.insert(CNOT(qubits[index], qubits[n]))
    prog.insert(circuit)
    return prog
