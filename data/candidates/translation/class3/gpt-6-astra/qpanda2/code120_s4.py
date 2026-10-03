# EVAL_META: task_id=120, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
atexit.register(lambda: machine.finalize())


def create_diagonal_circuit(diag):
    values = np.asarray(diag, dtype=complex)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("diag must be a nonempty one-dimensional sequence.")
    size = int(values.size)
    if size & (size - 1):
        raise ValueError("The length of diag must be a power of two.")
    if not np.all(np.isfinite(values)) or not np.allclose(np.abs(values), 1):
        raise ValueError("Every diagonal element must have unit magnitude.")

    num_qubits = size.bit_length() - 1
    while len(qubits) < max(1, num_qubits):
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()

    if num_qubits == 0:
        phase = float(np.angle(values[0]))
        circuit << pq.U1(qubits[0], phase)
        circuit << pq.X(qubits[0])
        circuit << pq.U1(qubits[0], phase)
        circuit << pq.X(qubits[0])
    else:
        active = qubits[:num_qubits]
        for qubit in active:
            circuit << pq.I(qubit)

        for basis, value in enumerate(values):
            phase = float(np.angle(value))
            if phase == 0.0:
                continue

            flipped = [
                active[bit]
                for bit in range(num_qubits)
                if not ((basis >> bit) & 1)
            ]
            for qubit in flipped:
                circuit << pq.X(qubit)

            gate = pq.U1(active[-1], phase)
            if num_qubits > 1:
                gate = gate.control(active[:-1])
            circuit << gate

            for qubit in reversed(flipped):
                circuit << pq.X(qubit)

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
