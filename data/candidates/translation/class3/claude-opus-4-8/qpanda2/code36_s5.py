# EVAL_META: task_id=36, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(64)

def bv_function(s):
    n = len(s)
    qc = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc << CNOT(qubits[index], qubits[n])
    return qc

machine.finalize()
