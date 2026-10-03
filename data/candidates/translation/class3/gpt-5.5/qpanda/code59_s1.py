# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, H, CNOT

def create_cz_gate():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit << H(qubits[1]) << CNOT(qubits[0], qubits[1]) << H(qubits[1])
    circuit._machine = machine
    return circuit
