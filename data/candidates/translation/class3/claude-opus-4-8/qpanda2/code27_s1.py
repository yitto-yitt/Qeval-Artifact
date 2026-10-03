# EVAL_META: task_id=27, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, qAlloc_many, H, CNOT, circuit_to_originir

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(3)


def apply_op_back():
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << CNOT(qubits[0], qubits[1])
    circuit << H(qubits[0])
    return circuit


machine.finalize()
