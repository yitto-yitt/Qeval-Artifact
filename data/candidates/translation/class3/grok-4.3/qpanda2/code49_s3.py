# EVAL_META: task_id=49, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def simple_elitzur_vaidman():
    circuit = QCircuit()
    circuit << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << H(qubits[0])
    return circuit

machine.finalize()
