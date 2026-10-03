# EVAL_META: task_id=36, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(100)

def bv_function(s):
    n = len(s)
    circuit = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit << CNOT(global_qubits[index], global_qubits[n])
    return circuit

machine.finalize()
