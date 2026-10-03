# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep(num_qubits):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(num_qubits)
    prog = pq.QProg()
    if num_qubits > 0:
        prog << pq.X(qubits[0])
    return prog
