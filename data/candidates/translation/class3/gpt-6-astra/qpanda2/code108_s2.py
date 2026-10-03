# EVAL_META: task_id=108, framework=qpanda2, class=3
import atexit
import math
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)


def initialize_adjoint_and_compose(data1, data2):
    def as_matrix(data):
        if hasattr(data, "data") and not isinstance(data, np.ndarray):
            data = data.data
        matrix = np.asarray(data, dtype=np.complex128)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("A Choi matrix must be a square matrix.")
        dimension = math.isqrt(matrix.shape[0])
        if dimension * dimension != matrix.shape[0] or dimension == 0:
            raise ValueError("Cannot infer equal input and output dimensions.")
        return matrix, dimension

    first, dimension = as_matrix(data1)
    second, second_dimension = as_matrix(data2)
    if dimension != second_dimension:
        raise ValueError("The channel dimensions are incompatible.")

    bits = max(1, (dimension - 1).bit_length())
    if 8 * bits > len(qubits):
        raise ValueError("The channel exceeds the allocated quantum register.")
    padded_dimension = 1 << bits
    register_size = 4 * bits

    def padded_vector(matrix):
        tensor = np.zeros(
            (padded_dimension,) * 4, dtype=np.complex128
        )
        tensor[:dimension, :dimension, :dimension, :dimension] = (
            matrix.reshape((dimension,) * 4)
        )
        return tensor.ravel()

    def prepare(vector, register):
        circuit = pq.QCircuit()
        norm = float(np.linalg.norm(vector))
        if norm == 0:
            return circuit, norm
        amplitudes = vector / norm
        count = len(register)

        for level in range(count):
            target = register[count - level - 1]
            controls = [register[count - position - 1]
                        for position in range(level)]
            width = 1 << (count - level)
            for prefix in range(1 << level):
                start = prefix * width
                half = width // 2
                left = float(np.linalg.norm(amplitudes[start:start + half]))
                right = float(
                    np.linalg.norm(amplitudes[start + half:start + width])
                )
                if left == 0 and right == 0:
                    continue
                angle = 2 * math.atan2(right, left)
                if angle == 0:
                    continue
                inverted = [
                    controls[position]
                    for position in range(level)
                    if not ((prefix >> (level - position - 1)) & 1)
                ]
                for qubit in inverted:
                    circuit << pq.X(qubit)
                gate = pq.RY(target, angle)
                if controls:
                    gate = gate.control(controls)
                circuit << gate
                for qubit in reversed(inverted):
                    circuit << pq.X(qubit)

        for index, amplitude in enumerate(amplitudes):
            if amplitude == 0:
                continue
            phase = float(np.angle(amplitude))
            if phase == 0:
                continue
            inverted = [
                register[position]
                for position in range(count)
                if not ((index >> position) & 1)
            ]
            for qubit in inverted:
                circuit << pq.X(qubit)
            gate = pq.U1(register[0], phase)
            if count > 1:
                gate = gate.control(register[1:])
            circuit << gate
            for qubit in reversed(inverted):
                circuit << pq.X(qubit)

        return circuit, norm

    def execute(circuit):
        program = pq.QProg()
        program << circuit
        machine.directly_run(program)
        return np.asarray(machine.get_qstate(), dtype=np.complex128)

    def extract_channel(state, scale):
        tensor = state[:1 << register_size].reshape(
            (padded_dimension,) * 4
        )
        return (
            tensor[:dimension, :dimension, :dimension, :dimension]
            .reshape(first.shape)
            .copy() * scale
        )

    first_vector = padded_vector(first)
    second_vector = padded_vector(second)
    first_register = qubits[:register_size]
    second_register = qubits[register_size:2 * register_size]

    first_circuit, first_norm = prepare(first_vector, first_register)
    choi1 = extract_channel(execute(first_circuit), first_norm)

    adjoint_circuit, adjoint_norm = prepare(
        first_vector.conjugate(), first_register
    )
    for position in range(bits):
        adjoint_circuit << pq.SWAP(
            qubits[3 * bits + position], qubits[2 * bits + position]
        )
        adjoint_circuit << pq.SWAP(
            qubits[bits + position], qubits[position]
        )
    adjoint_choi1 = extract_channel(
        execute(adjoint_circuit), adjoint_norm
    )

    second_circuit, second_norm = prepare(second_vector, second_register)
    composition_circuit = pq.QCircuit()
    composition_circuit << first_circuit
    composition_circuit << second_circuit
    for position in range(bits):
        composition_circuit << pq.CNOT(
            qubits[2 * bits + position], qubits[7 * bits + position]
        )
        composition_circuit << pq.H(qubits[2 * bits + position])
        composition_circuit << pq.CNOT(
            qubits[position], qubits[5 * bits + position]
        )
        composition_circuit << pq.H(qubits[position])

    composition_state = execute(composition_circuit)
    input_row, output_row, input_column, output_column = np.indices(
        (dimension,) * 4, dtype=np.int64
    )
    indices = (
        (input_row << (3 * bits))
        | (output_row << (6 * bits))
        | (input_column << bits)
        | (output_column << (4 * bits))
    )
    composed_choi = (
        composition_state[indices].reshape(first.shape)
        * first_norm * second_norm * padded_dimension
    )
    return choi1, adjoint_choi1, composed_choi


atexit.register(machine.finalize)
