# EVAL_META: task_id=62, framework=qpanda, class=2
import pyqpanda3.core as pq


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    prog = pq.QProg()
    for i in range(num_qubits):
        if state[i] == 1:
            prog.insert(pq.X(qubits[i]))
        if basis[i] == 1:
            prog.insert(pq.H(qubits[i]))
    # Attach machine to the returned program to prevent garbage collection
    prog.machine = machine
    return prog
