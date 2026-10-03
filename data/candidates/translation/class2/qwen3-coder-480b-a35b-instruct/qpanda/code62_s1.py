# EVAL_META: task_id=62, framework=qpanda, class=2
from pyqpanda import *


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    machine = init(QMachineType.CPU)
    qubits = machine.qAlloc_many(num_qubits)
    circuit = QCircuit()
    for i in range(len(basis)):
        if state[i] == 1:
            circuit.insert(X(qubits[i]))
        if basis[i] == 1:
            circuit.insert(H(qubits[i]))
    return circuit
