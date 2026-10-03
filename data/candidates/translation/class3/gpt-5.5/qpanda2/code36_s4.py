# EVAL_META: task_id=36, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(64)

def bv_function(s):
    n = len(s)
    circuit = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit << CNOT(_qubits[index], _qubits[n])
    return circuit

atexit.register(lambda: machine.finalize())
