# EVAL_META: task_id=120, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(0)
atexit.register(machine.finalize)


def create_diagonal_circuit(diag):
    diagonal = np.asarray(diag, dtype=complex)
    if diagonal.ndim != 1:
        raise ValueError("diag must be a one-dimensional sequence.")

    size = len(diagonal)
    if size < 2 or size & (size - 1):
        raise ValueError("The diagonal length must be a power of two, at least two.")
    if not np.allclose(np.abs(diagonal), 1.0):
        raise ValueError("All diagonal entries must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    while len(qubits) < num_qubits:
        qubits.append(machine.qAlloc())

    active = qubits[:num_qubits]
    circuit = pq.QCircuit()

    for basis_state, entry in enumerate(diagonal):
        angle = float(np.angle(entry))
        if angle == 0.0:
            continue

        zero_bits = [
            index for index in range(num_qubits)
            if not ((basis_state >> index) & 1)
        ]
        for index in zero_bits:
            circuit << pq.X(active[index])

        phase_gate = pq.U1(active[0], angle)
        if num_qubits > 1:
            phase_gate = phase_gate.control(active[1:])
        circuit << phase_gate

        for index in reversed(zero_bits):
            circuit << pq.X(active[index])

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
