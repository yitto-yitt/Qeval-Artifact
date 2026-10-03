# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import *

def controlled_custom_unitary_circuit():
    if not hasattr(controlled_custom_unitary_circuit, "_machine"):
        machine = CPUQVM()
        if hasattr(machine, "init_qvm"):
            machine.init_qvm()
        elif hasattr(machine, "init"):
            machine.init()
        controlled_custom_unitary_circuit._machine = machine
        controlled_custom_unitary_circuit._qubits = machine.qAlloc_many(2)

    q = controlled_custom_unitary_circuit._qubits
    qc = QCircuit()
    custom_gate = U3(q[1], 0.3, 0.2, 0.1).control([q[0]])
    qc << custom_gate
    return qc
