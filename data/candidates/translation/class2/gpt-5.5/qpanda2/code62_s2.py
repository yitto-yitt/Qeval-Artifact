# EVAL_META: task_id=62, framework=qpanda2, class=2
from pyqpanda import *


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)

    circuit = QCircuit()
    for i in range(len(basis)):
        if state[i] == 1:
            circuit.insert(X(qubits[i]))
        if basis[i] == 1:
            circuit.insert(H(qubits[i]))

    if not hasattr(bb84_senders_circuit, "_machines"):
        bb84_senders_circuit._machines = []
    bb84_senders_circuit._machines.append(machine)

    return circuit
