# EVAL_META: task_id=0, framework=qpanda2, class=3
from pyqpanda import *
import atexit

init(QMachineType.CPU)
qvm = CPUQVM()
qvm.init()
atexit.register(qvm.finalize)

def create_quantum_circuit(n_qubits):
    qubits = qvm.qAlloc_many(n_qubits)
    circuit = QCircuit()
    for q in qubits:
        circuit << I(q)
    return circuit
