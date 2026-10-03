# EVAL_META: task_id=36, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, CNOT

machine = CPUQVM()
machine.init_qvm()

def bv_function(s):
    n = len(s)
    qubits = machine.qAlloc_many(n + 1)
    qc = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc << CNOT(qubits[index], qubits[n])
    return qc

machine.finalize()
