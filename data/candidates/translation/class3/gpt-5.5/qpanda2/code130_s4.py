# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(64)

def inv_circuit(n):
    if n < 5:
        raise ValueError("n must be at least 5")
    if n > len(q):
        raise ValueError("n exceeds globally allocated qubits")

    qc = QCircuit()
    for i in range(2):
        qc.insert(H(q[i + 1]))

    for i in range(2):
        qc.insert(CNOT(q[i + 1], q[i + 3]))

    return qc.dagger()

atexit.register(machine.finalize)
