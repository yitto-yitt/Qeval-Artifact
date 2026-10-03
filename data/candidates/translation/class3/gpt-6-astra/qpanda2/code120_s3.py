# EVAL_META: task_id=120, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)


def create_diagonal_circuit(diag):
    values = np.asarray(diag, dtype=complex)
    if values.ndim != 1:
        raise ValueError("diag must be a one-dimensional sequence.")

    size = len(values)
    if size < 2 or size & (size - 1):
        raise ValueError("The number of diagonal entries must be a power of two.")
    if not np.all(np.isfinite(values)) or not np.allclose(np.abs(values), 1.0):
        raise ValueError("Every diagonal entry must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    if num_qubits > len(qubits):
        raise ValueError("The diagonal exceeds the allocated quantum register.")

    register = qubits[:num_qubits]
    circuit = pq.QCircuit()

    for basis, value in enumerate(values):
        angle = float(np.angle(value))
        if angle == 0.0:
            continue

        zero_bits = [
            bit for bit in range(num_qubits)
            if not (basis & (1 << bit))
        ]
        for bit in zero_bits:
            circuit << pq.X(register[bit])

        phase_gate = pq.U1(register[0], angle)
        if num_qubits > 1:
            phase_gate = phase_gate.control(register[1:])
        circuit << phase_gate

        for bit in reversed(zero_bits):
            circuit << pq.X(register[bit])

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(machine.finalize)
