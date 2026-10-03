# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import *

def bv_function(s):
    n = len(s)
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(n + 1)
    circuit = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit << CNOT(qubits[index], qubits[n])
    return circuit
