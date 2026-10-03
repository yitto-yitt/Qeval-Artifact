# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)

def inv_circuit(n):
    prog = QCircuit()
    for i in range(2):
        prog << H(qubits[i + 1])
    for i in range(2):
        prog << CNOT(qubits[i + 1], qubits[i + 2 + 1])
    return prog.dagger()

machine.finalize()
