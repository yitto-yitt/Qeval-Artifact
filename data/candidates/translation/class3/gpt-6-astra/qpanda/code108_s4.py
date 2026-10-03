# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def initialize_adjoint_and_compose(data1, data2):
    def as_choi(data):
        matrix = np.asarray(data, dtype=complex)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("A Choi matrix must be square.")
        dimension = int(round(np.sqrt(matrix.shape[0])))
        if dimension * dimension != matrix.shape[0]:
            raise ValueError("Cannot infer equal input and output dimensions.")
        return matrix.copy(), dimension

    def preparation(vector, qubits):
        vector = np.asarray(vector, dtype=complex).ravel()
        norm = np.linalg.norm(vector)
        state = vector / norm if norm else np.eye(1, vector.size, 0).ravel()
        phase = state[0] / abs(state[0]) if abs(state[0]) else 1.0
        reflector = state.copy()
        reflector[0] += phase
        unitary = -phase * (
            np.eye(state.size, dtype=complex)
            - 2.0 * np.outer(reflector, reflector.conj())
            / np.vdot(reflector, reflector).real
        )
        errors = []
        for name in ("QOracle", "matrix_decompose"):
            constructor = getattr(pq, name, None)
            if constructor is None:
                continue
            for matrix in (unitary, unitary.tolist()):
                try:
                    return constructor(qubits, matrix), norm
                except (TypeError, ValueError, RuntimeError) as error:
                    errors.append(error)
        if errors:
            raise errors[-1]
        raise RuntimeError("The framework does not expose matrix-based gates.")

    def execute(program):
        simulator = pq.CPUQVM()
        initializer = getattr(simulator, "init_qvm", None)
        if callable(initializer):
            initializer()
        result = simulator.run(program, 1)
        holders = [simulator, result]
        accessor = getattr(simulator, "result", None)
        if accessor is not None:
            holders.append(accessor() if callable(accessor) else accessor)
        for holder in holders:
            if holder is None:
                continue
            for name in (
                "get_state_vector",
                "get_statevector",
                "get_qstate",
                "state_vector",
                "statevector",
            ):
                accessor = getattr(holder, name, None)
                if accessor is None:
                    continue
                try:
                    state = accessor() if callable(accessor) else accessor
                    if isinstance(state, dict):
                        vector = np.zeros(1 << program.qubit_num(), dtype=complex)
                        for key, value in state.items():
                            index = int(key, 2) if isinstance(key, str) else int(key)
                            vector[index] = value
                        return vector
                    return np.asarray(state, dtype=complex).ravel()
                except (TypeError, ValueError, AttributeError):
                    continue
        raise RuntimeError("The simulator did not expose its state vector.")

    choi1, dimension1 = as_choi(data1)
    choi2, dimension2 = as_choi(data2)
    if dimension1 != dimension2:
        raise ValueError("The channel dimensions are incompatible for composition.")

    dimension = dimension1
    bits = max(1, (dimension - 1).bit_length())
    padded_dimension = 1 << bits

    def padded_vector(matrix):
        tensor = np.zeros((padded_dimension,) * 4, dtype=complex)
        tensor[:dimension, :dimension, :dimension, :dimension] = matrix.reshape(
            (dimension,) * 4
        )
        return tensor.ravel()

    vector1 = padded_vector(choi1)
    vector2 = padded_vector(choi2)

    adjoint_program = pq.QProg()
    gate, norm1 = preparation(vector1.conj(), list(range(4 * bits)))
    adjoint_program << gate
    for bit in range(bits):
        adjoint_program << pq.SWAP(3 * bits + bit, 2 * bits + bit)
        adjoint_program << pq.SWAP(bits + bit, bit)
    adjoint_tensor = execute(adjoint_program).reshape((padded_dimension,) * 4)
    adjoint = (
        norm1
        * adjoint_tensor[:dimension, :dimension, :dimension, :dimension]
    ).reshape(choi1.shape)

    composition_program = pq.QProg()
    first_gate, norm1 = preparation(
        vector1, list(range(4 * bits, 8 * bits))
    )
    second_gate, norm2 = preparation(vector2, list(range(4 * bits)))
    composition_program << first_gate << second_gate

    for bit in range(bits):
        composition_program << pq.CNOT(6 * bits + bit, 3 * bits + bit)
        composition_program << pq.H(6 * bits + bit)
        composition_program << pq.CNOT(4 * bits + bit, bits + bit)
        composition_program << pq.H(4 * bits + bit)

    joint_state = execute(composition_program).reshape((padded_dimension,) * 8)
    contracted = joint_state[:, 0, :, 0, 0, :, 0, :].transpose(0, 2, 1, 3)
    composed = (
        padded_dimension
        * norm1
        * norm2
        * contracted[:dimension, :dimension, :dimension, :dimension]
    ).reshape(choi1.shape)

    return choi1, adjoint, composed
