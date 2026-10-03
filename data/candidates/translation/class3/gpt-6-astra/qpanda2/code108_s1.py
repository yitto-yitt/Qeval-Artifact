# EVAL_META: task_id=108, framework=qpanda2, class=3
import atexit
import math
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = list(machine.qAlloc_many(2))


def initialize_adjoint_and_compose(data1, data2):
    def read_choi(data):
        if hasattr(data, "input_dims") and hasattr(data, "output_dims"):
            matrix = np.asarray(data.data, dtype=np.complex128)
            din = math.prod(data.input_dims())
            dout = math.prod(data.output_dims())
        else:
            matrix = np.asarray(data, dtype=np.complex128)
            if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
                raise ValueError("Choi data must be a square matrix.")
            din = dout = math.isqrt(matrix.shape[0])

        if din < 1 or dout < 1 or matrix.shape != (din * dout, din * dout):
            raise ValueError("Invalid Choi matrix dimensions.")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("Choi data must contain finite values.")

        superoperator = matrix.reshape(din, dout, din, dout)
        superoperator = superoperator.transpose(1, 3, 0, 2)
        return superoperator.reshape(dout * dout, din * din), din, dout

    s1, din1, dout1 = read_choi(data1)
    s2, din2, dout2 = read_choi(data2)
    if dout1 != din2:
        raise ValueError("The channel dimensions are incompatible for composition.")

    largest_dimension = max(din1 * din1, dout1 * dout1,
                            din2 * din2, dout2 * dout2)
    work_count = (largest_dimension - 1).bit_length()
    work_dimension = 1 << work_count

    while len(qubits) < work_count + 2:
        qubits.append(machine.qAlloc())

    calibration_matrix = np.array(
        [[0, 1, 0, 0],
         [1, 0, 0, 0],
         [0, 0, 0, 1],
         [0, 0, 1, 0]],
        dtype=np.complex128,
    )
    calibration = pq.QProg()
    calibration << pq.QOracle(qubits[:2], calibration_matrix)
    machine.directly_run(calibration)
    calibration_state = np.asarray(machine.get_qstate(), dtype=np.complex128)
    reverse_targets = int(np.argmax(np.abs(calibration_state))) == 2

    def oracle_targets(flag):
        targets = qubits[:work_count] + [qubits[flag]]
        return targets[::-1] if reverse_targets else targets

    def block_encoding(matrix):
        padded = np.zeros((work_dimension, work_dimension), dtype=np.complex128)
        padded[:matrix.shape[0], :matrix.shape[1]] = matrix
        left, singular_values, right_h = np.linalg.svd(padded)
        scale = max(1.0, float(singular_values[0]))
        normalized = padded / scale
        residual = np.sqrt(np.maximum(0.0, 1.0 - (singular_values / scale) ** 2))
        upper_right = (left * residual) @ left.conj().T
        lower_left = (right_h.conj().T * residual) @ right_h
        unitary = np.block([
            [normalized, upper_right],
            [lower_left, -normalized.conj().T],
        ])
        return unitary, scale

    unitary1, scale1 = block_encoding(s1)
    unitary2, scale2 = block_encoding(s2)
    gate1 = pq.QOracle(oracle_targets(work_count), unitary1)
    gate1_adjoint = gate1.dagger()
    gate2 = pq.QOracle(oracle_targets(work_count + 1), unitary2)

    def execute_columns(gates, rows, columns, scale):
        result = np.empty((rows, columns), dtype=np.complex128)
        for column in range(columns):
            program = pq.QProg()
            for bit in range(work_count):
                if (column >> bit) & 1:
                    program << pq.X(qubits[bit])
            for gate in gates:
                program << gate
            machine.directly_run(program)
            state = np.asarray(machine.get_qstate(), dtype=np.complex128)
            result[:, column] = state[:rows] * scale
        return result

    recovered1 = execute_columns(
        [gate1], dout1 * dout1, din1 * din1, scale1
    )
    recovered_adjoint = execute_columns(
        [gate1_adjoint], din1 * din1, dout1 * dout1, scale1
    )
    recovered_composition = execute_columns(
        [gate1, gate2], dout2 * dout2, din1 * din1, scale1 * scale2
    )

    def as_choi(superoperator, din, dout):
        return (
            superoperator.reshape(dout, dout, din, din)
            .transpose(2, 0, 3, 1)
            .reshape(din * dout, din * dout)
            .copy()
        )

    return (
        as_choi(recovered1, din1, dout1),
        as_choi(recovered_adjoint, dout1, din1),
        as_choi(recovered_composition, din1, dout2),
    )


atexit.register(lambda: machine.finalize())
