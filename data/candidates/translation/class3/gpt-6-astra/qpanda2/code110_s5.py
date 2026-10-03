# EVAL_META: task_id=110, framework=qpanda2, class=3
import atexit
import random
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(24)


def equivalent_clifford_circuit(circuit, n):
    original_program = pq.QProg()
    original_program << circuit
    original = np.asarray(pq.get_matrix(original_program), dtype=complex)
    dimension = int(round(np.sqrt(original.size)))
    original = original.reshape(dimension, dimension)
    num_qubits = dimension.bit_length() - 1

    if dimension != 1 << num_qubits:
        raise ValueError("The circuit matrix must have a power-of-two dimension.")
    if num_qubits > len(qubits):
        raise ValueError("The circuit exceeds the allocated quantum register.")

    results = []
    while len(results) < n:
        candidate = pq.QCircuit()
        for qubit in qubits[:num_qubits]:
            candidate << pq.I(qubit)

        if num_qubits:
            for _ in range(24 * num_qubits * num_qubits):
                gate_type = random.randrange(7 if num_qubits > 1 else 6)
                target = random.randrange(num_qubits)
                if gate_type == 0:
                    candidate << pq.H(qubits[target])
                elif gate_type == 1:
                    candidate << pq.S(qubits[target])
                elif gate_type == 2:
                    candidate << pq.X(qubits[target])
                elif gate_type == 3:
                    candidate << pq.Y(qubits[target])
                elif gate_type == 4:
                    candidate << pq.Z(qubits[target])
                elif gate_type == 5:
                    candidate << pq.I(qubits[target])
                else:
                    control = random.randrange(num_qubits - 1)
                    if control >= target:
                        control += 1
                    candidate << pq.CNOT(qubits[control], qubits[target])

        candidate_program = pq.QProg()
        candidate_program << candidate
        matrix = np.asarray(
            pq.get_matrix(candidate_program), dtype=complex
        ).reshape(dimension, dimension)

        pivot = int(np.argmax(np.abs(matrix)))
        phase = np.angle(matrix.flat[pivot]) - np.angle(original.flat[pivot])
        aligned_original = np.exp(1j * phase) * original

        if np.allclose(matrix, aligned_original, rtol=0.4, atol=0.4):
            results.append(candidate)

    return results


atexit.register(machine.finalize)
