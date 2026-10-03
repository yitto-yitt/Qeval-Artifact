# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import QProg, QCircuit, H, CR, QMachineType, init_quantum_machine, destroy_quantum_machine

def qft_no_swaps(num_qubits):
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(num_qubits)
    circuit = QCircuit()
    for j in range(num_qubits):
        for k in range(j):
            angle = -3.141592653589793 / (2 ** (j - k))
            circuit << CR(qubits[j], qubits[k], angle)
        circuit << H(qubits[j])
    prog = QProg()
    prog << circuit
    destroy_quantum_machine(machine)
    return circuit
