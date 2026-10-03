# EVAL_META: task_id=36, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(32)
atexit.register(machine.finalize)

def bv_function(s):
    n = len(s)
    if n + 1 > len(qubits):
        raise ValueError("Input bitstring is too long for the allocated qubit register.")
    qc = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.insert(CNOT(qubits[index], qubits[n]))
    return qc
