# EVAL_META: task_id=59, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, qAlloc_many, H, CNOT, finalize

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(2)

def create_cz_gate():
    circuit = QCircuit()
    circuit << H(qubits[1])
    circuit << CNOT(qubits[0], qubits[1])
    circuit << H(qubits[1])
    return circuit

machine.finalize()
