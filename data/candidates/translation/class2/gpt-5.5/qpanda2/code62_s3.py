# EVAL_META: task_id=62, framework=qpanda2, class=2
import pyqpanda as pq


def bb84_senders_circuit(state, basis):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(len(state))
    circuit = pq.QCircuit()

    for i in range(len(basis)):
        if state[i] == 1:
            circuit.insert(pq.X(qubits[i]))
        if basis[i] == 1:
            circuit.insert(pq.H(qubits[i]))

    circuit._machine = machine
    circuit._qubits = qubits
    return circuit
