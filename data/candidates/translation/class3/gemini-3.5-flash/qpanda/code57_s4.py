# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, qAllocMany, init_quantum_machine, QMachineType

def create_swap_gate():
    try:
        init_quantum_machine(QMachineType.CPU)
    except Exception:
        pass
    qubits = qAllocMany(2)
    circuit = QCircuit()
    circuit << CNOT(qubits[0], qubits[1]) \
            << CNOT(qubits[1], qubits[0]) \
            << CNOT(qubits[0], qubits[1])
    return circuit
