# EVAL_META: task_id=62, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QCircuit, X, H


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    machine = CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    circuit = QCircuit()
    for i in range(len(basis)):
        if state[i] == 1:
            circuit << X(qubits[i])
        if basis[i] == 1:
            circuit << H(qubits[i])
    if not hasattr(bb84_senders_circuit, "_resources"):
        bb84_senders_circuit._resources = []
    bb84_senders_circuit._resources.append((machine, qubits))
    return circuit
