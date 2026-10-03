# EVAL_META: task_id=108, framework=qpanda, class=3
import math
import numpy as np
import pyqpanda3.core as pq


def initialize_adjoint_and_compose(data1, data2):
    def read_choi(data):
        if isinstance(data, (np.ndarray, list, tuple)):
            matrix = np.asarray(data, dtype=complex)
        else:
            matrix = np.asarray(data.data, dtype=complex)

        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("A Choi matrix must be square.")

        if callable(getattr(data, "input_dims", None)):
            din = math.prod(data.input_dims())
            dout = math.prod(data.output_dims())
        else:
            din = dout = math.isqrt(matrix.shape[0])

        if din * dout != matrix.shape[0]:
            raise ValueError("Cannot infer valid channel dimensions.")
        return matrix.copy(), din, dout

    def oracle(qubits, matrix):
        last_error = None
        for representation in (
            matrix,
            matrix.reshape(-1).tolist(),
            matrix.tolist(),
        ):
            try:
                return pq.QOracle(qubits, representation)
            except (TypeError, ValueError, RuntimeError) as error:
                last_error = error
        raise last_error

    def run_state(program):
        machine = pq.CPUQVM()
        initializer = getattr(machine, "init_qvm", None)
        if callable(initializer):
            initializer()

        try:
            returned = machine.run(program, 1)
        except TypeError:
            returned = machine.run(program)

        owners = [machine, returned]
        result = getattr(machine, "result", None)
        if result is not None:
            owners.insert(0, result() if callable(result) else result)

        for owner in owners:
            if owner is None:
                continue
            for name in (
                "get_state_vector",
                "get_qstate",
                "get_state",
                "state_vector",
            ):
                accessor = getattr(owner, name, None)
                if accessor is None:
                    continue
                state = accessor() if callable(accessor) else accessor
                if isinstance(state, dict):
                    width = max(len(str(key)) for key in state)
                    vector = np.zeros(1 << width, dtype=complex)
                    for key, amplitude in state.items():
                        index = int(key, 2) if isinstance(key, str) else int(key)
                        vector[index] = amplitude
                    return vector
                return np.asarray(state, dtype=complex).reshape(-1)
        raise RuntimeError("The simulator did not expose its state vector.")

    choi1, din1, dout1 = read_choi(data1)
    choi2, din2, dout2 = read_choi(data2)
    if dout1 != din2:
        raise ValueError("The channel dimensions are incompatible for composition.")

    def to_superoperator(matrix, din, dout):
        return matrix.reshape(din, dout, din, dout).transpose(
            1, 3, 0, 2
        ).reshape(dout * dout, din * din)

    def to_choi(matrix, din, dout):
        return matrix.reshape(dout, dout, din, din).transpose(
            2, 0, 3, 1
        ).reshape(din * dout, din * dout)

    super1 = to_superoperator(choi1, din1, dout1)
    super2 = to_superoperator(choi2, din2, dout2)
    largest_dimension = max(*super1.shape, *super2.shape)
    data_qubit_count = (largest_dimension - 1).bit_length()
    size = 1 << data_qubit_count

    def block_encoding(matrix):
        padded = np.zeros((size, size), dtype=complex)
        padded[:matrix.shape[0], :matrix.shape[1]] = matrix
        left, singular, right_h = np.linalg.svd(padded)
        scale = max(1.0, float(singular[0]))
        normalized = padded / scale
        residual = np.sqrt(np.maximum(0.0, 1.0 - (singular / scale) ** 2))
        left_root = (left * residual) @ left.conj().T
        right_root = (right_h.conj().T * residual) @ right_h
        unitary = np.block([
            [normalized, left_root],
            [right_root, -normalized.conj().T],
        ])
        return unitary, scale

    unitary1, scale1 = block_encoding(super1)
    unitary2, scale2 = block_encoding(super2)

    calibration = pq.QProg()
    calibration << oracle(
        [0, 1],
        np.kron(np.eye(2), np.array([[0, 1], [1, 0]], dtype=complex)),
    )
    calibration_state = run_state(calibration)
    marked_index = int(np.argmax(np.abs(calibration_state)))
    if marked_index not in (1, 2):
        raise RuntimeError("Unexpected oracle qubit ordering.")
    reverse_oracle_qubits = marked_index == 2

    def append_oracle(program, qubits, matrix):
        if reverse_oracle_qubits:
            qubits = list(reversed(qubits))
        program << oracle(qubits, matrix)

    data_qubits = list(range(data_qubit_count))
    first_register = data_qubits + [data_qubit_count]
    second_register = data_qubits + [data_qubit_count + 1]

    def simulate_block(operations, rows, columns, scale):
        matrix = np.empty((rows, columns), dtype=complex)
        for column in range(columns):
            program = pq.QProg()
            for bit in range(data_qubit_count):
                if (column >> bit) & 1:
                    program << pq.X(bit)
            for register, unitary in operations:
                append_oracle(program, register, unitary)
            state = run_state(program)
            matrix[:, column] = scale * state[:rows]
        return matrix

    adjoint_super = simulate_block(
        [(first_register, unitary1.conj().T)],
        din1 * din1,
        dout1 * dout1,
        scale1,
    )
    composed_super = simulate_block(
        [(first_register, unitary1), (second_register, unitary2)],
        dout2 * dout2,
        din1 * din1,
        scale1 * scale2,
    )

    adjoint_choi1 = to_choi(adjoint_super, dout1, din1)
    composed_choi = to_choi(composed_super, din1, dout2)
    return choi1, adjoint_choi1, composed_choi
