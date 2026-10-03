# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, CNOT

def create_swap_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    circuit = QCircuit()
    circuit << CNOT(qubits[0], qubits[1]) \
            << CNOT(qubits[1], qubits[0]) \
            << CNOT(qubits[0], qubits[1])
    # Keep a reference to the virtual machine to prevent resource deallocation
    circuit._qvm = qvm
    return circuit
