# EVAL_META: task_id=36, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, CNOT

machine = CPUQVM()
machine.set_configure(64, 64)
machine.init_qvm()
qubits = machine.qAlloc_many(64)
atexit.register(machine.finalize)


def bv_function(s):
    n = len(s)
    if n + 1 > len(qubits):
        raise ValueError("The oracle exceeds the allocated qubit capacity.")

    oracle = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            oracle << CNOT(qubits[index], qubits[n])
    return oracle
