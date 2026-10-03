# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    num_params = num_qubits * 2 * (reps + 1)
    params = [np.pi / 4] * num_params

    prog = pq.QProg()
    idx = 0

    def su2_layer():
        nonlocal idx
        for q in range(num_qubits):
            prog.insert(pq.RY(qubits[q], params[idx]))
            idx += 1
        for q in range(num_qubits):
            prog.insert(pq.RZ(qubits[q], params[idx]))
            idx += 1

    def entangle_layer():
        for q in range(num_qubits - 1):
            prog.insert(pq.CNOT(qubits[q], qubits[q + 1]))

    for r in range(reps):
        su2_layer()
        prog.insert(pq.BARRIER(qubits))
        entangle_layer()
        prog.insert(pq.BARRIER(qubits))
    su2_layer()

    return prog


if __name__ == "__main__":
    circuit = create_efficientSU2()
    print(circuit)
    machine.finalize()
