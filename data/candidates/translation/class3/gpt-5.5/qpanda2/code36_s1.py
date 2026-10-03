# EVAL_META: task_id=36, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.set_configure(256, 256)
machine.init_qvm()
qubits = machine.qAlloc_many(256)
atexit.register(machine.finalize)

def bv_function(s):
    n = len(s)
    qc = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc << CNOT(qubits[index], qubits[n])
    return qc
