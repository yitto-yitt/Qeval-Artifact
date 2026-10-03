# EVAL_META: task_id=62, framework=qpanda2, class=2
import pyqpanda as pq


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(num_qubits)
    prog = pq.QProg()
    for i in range(len(basis)):
        if state[i] == 1:
            prog << pq.X(q[i])
        if basis[i] == 1:
            prog << pq.H(q[i])
    return prog
