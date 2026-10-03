# EVAL_META: task_id=62, framework=qpanda, class=2
import pyqpanda3.core as pq

_bb84_sender_machines = []


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)

    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    qubits = machine.qAlloc_many(num_qubits)
    circuit = pq.QCircuit()

    for i in range(len(basis)):
        if state[i] == 1:
            circuit << pq.X(qubits[i])
        if basis[i] == 1:
            circuit << pq.H(qubits[i])

    _bb84_sender_machines.append((machine, qubits))
    return circuit
