# EVAL_META: task_id=62, framework=qpanda2, class=2
import pyqpanda as pq


def bb84_senders_circuit(state, basis):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(len(state)) if len(state) else []
    circuit = pq.QCircuit()

    for i in range(len(basis)):
        if state[i] == 1:
            circuit << pq.X(qubits[i])
        if basis[i] == 1:
            circuit << pq.H(qubits[i])

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)

    if not hasattr(bb84_senders_circuit, "_resources"):
        bb84_senders_circuit._resources = []
    bb84_senders_circuit._resources.append((machine, qubits, circuit))
    return circuit
