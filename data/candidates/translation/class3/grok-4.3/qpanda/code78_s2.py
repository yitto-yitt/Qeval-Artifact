# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import init_quantum_machine, QMachineType, QCircuit, H, CR
import math

def qft_no_swaps(num_qubits):
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(num_qubits)
    circuit = QCircuit()
    for i in range(num_qubits):
        for j in range(i):
            angle = -2 * math.pi / (2 ** (i - j))
            circuit << CR(qubits[j], qubits[i], angle)
        circuit << H(qubits[i])
    return circuit
