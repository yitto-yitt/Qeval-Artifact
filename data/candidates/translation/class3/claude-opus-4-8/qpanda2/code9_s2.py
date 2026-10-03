# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    num_params = (reps + 1) * 2 * num_qubits
    params = [np.pi / 4] * num_params

    prog = pq.QProg()
    idx = 0

    for r in range(reps):
        for q in range(num_qubits):
            prog << pq.RY(qubits[q], params[idx]); idx += 1
        for q in range(num_qubits):
            prog << pq.RZ(qubits[q], params[idx]); idx += 1
        prog << pq.BARRIER(qubits)
        for q in range(num_qubits - 1):
            prog << pq.CNOT(qubits[q], qubits[q + 1])
        prog << pq.BARRIER(qubits)

    for q in range(num_qubits):
        prog << pq.RY(qubits[q], params[idx]); idx += 1
    for q in range(num_qubits):
        prog << pq.RZ(qubits[q], params[idx]); idx += 1

    machine.directly_run(prog)
    result = machine.get_qstate()
    return result


if __name__ == "__main__":
    print(create_efficientSU2())
    machine.finalize()
