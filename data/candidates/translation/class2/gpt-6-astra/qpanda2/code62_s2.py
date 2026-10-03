# EVAL_META: task_id=62, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QCircuit, QProg, X, H


def bb84_senders_circuit(state, basis):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(len(state))
    circuit = QCircuit()

    for i in range(len(basis)):
        if state[i] == 1:
            circuit << X(qubits[i])
        if basis[i] == 1:
            circuit << H(qubits[i])

    program = QProg()
    program << circuit
    machine.directly_run(program)

    if not hasattr(bb84_senders_circuit, "_resources"):
        bb84_senders_circuit._resources = []
    bb84_senders_circuit._resources.append((machine, qubits, program))

    return circuit
