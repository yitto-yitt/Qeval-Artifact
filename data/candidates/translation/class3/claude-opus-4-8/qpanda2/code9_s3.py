# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, RY, RZ, CNOT, BARRIER
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def create_efficientSU2():
    num_qubits = 3
    reps = 1

    params = []
    param_idx = 0

    def next_param():
        nonlocal param_idx
        val = np.pi / 4 * (param_idx + 1)
        param_idx += 1
        params.append(val)
        return val

    circuit = QCircuit()

    for rep in range(reps):
        for q in range(num_qubits):
            circuit << RY(qubits[q], next_param())
        for q in range(num_qubits):
            circuit << RZ(qubits[q], next_param())

        circuit << BARRIER(qubits)

        for q in range(num_qubits - 1):
            circuit << CNOT(qubits[q], qubits[q + 1])

        circuit << BARRIER(qubits)

    for q in range(num_qubits):
        circuit << RY(qubits[q], next_param())
    for q in range(num_qubits):
        circuit << RZ(qubits[q], next_param())

    return circuit


if __name__ == "__main__":
    qc = create_efficientSU2()
    print(qc)
    machine.finalize()
