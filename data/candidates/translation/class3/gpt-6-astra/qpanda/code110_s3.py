# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, S, X, Z, CNOT


def equivalent_clifford_circuit(circuit, n):
    rng = np.random.default_rng()

    def statevector(program):
        simulator = CPUQVM()
        run_result = simulator.run(program, 1)
        sources = [simulator, run_result]
        if hasattr(simulator, "result"):
            result = simulator.result
            sources.append(result() if callable(result) else result)

        for source in sources:
            if source is None:
                continue
            for name in (
                "get_state_vector",
                "get_qstate",
                "get_statevector",
                "state_vector",
                "statevector",
                "get_state",
            ):
                if hasattr(source, name):
                    value = getattr(source, name)
                    value = value() if callable(value) else value
                    return np.asarray(value, dtype=complex).reshape(-1).copy()
        raise RuntimeError("The simulator does not expose its state vector.")

    original = QProg()
    original << circuit
    initial_column = statevector(original)
    dimension = initial_column.size
    num_qubits = dimension.bit_length() - 1
    if dimension != 1 << num_qubits:
        raise ValueError("Invalid state-vector dimension.")

    def unitary(program, first_column=None):
        matrix = np.empty((dimension, dimension), dtype=complex)
        for basis in range(dimension):
            if basis == 0 and first_column is not None:
                matrix[:, basis] = first_column
                continue
            prepared = QProg()
            if num_qubits:
                prepared << X(num_qubits - 1) << X(num_qubits - 1)
            for qubit in range(num_qubits):
                if (basis >> qubit) & 1:
                    prepared << X(qubit)
            prepared << program
            matrix[:, basis] = statevector(prepared)
        return matrix

    reference = unitary(original, initial_column)

    def random_clifford():
        elimination = QCircuit()

        for start in range(num_qubits):
            remaining = num_qubits - start
            while True:
                p_bits = rng.integers(0, 2, 2 * remaining)
                if np.any(p_bits):
                    break

            while True:
                q_bits = rng.integers(0, 2, 2 * remaining)
                pairing = (
                    np.dot(p_bits[:remaining], q_bits[remaining:])
                    + np.dot(p_bits[remaining:], q_bits[:remaining])
                )
                if int(pairing) & 1:
                    break

            px = np.zeros(num_qubits, dtype=np.int8)
            pz = np.zeros(num_qubits, dtype=np.int8)
            qx = np.zeros(num_qubits, dtype=np.int8)
            qz = np.zeros(num_qubits, dtype=np.int8)
            px[start:] = p_bits[:remaining]
            pz[start:] = p_bits[remaining:]
            qx[start:] = q_bits[:remaining]
            qz[start:] = q_bits[remaining:]

            def apply_h(qubit):
                elimination.__lshift__(H(qubit))
                px[qubit], pz[qubit] = pz[qubit], px[qubit]
                qx[qubit], qz[qubit] = qz[qubit], qx[qubit]

            def apply_s(qubit):
                elimination.__lshift__(S(qubit))
                pz[qubit] ^= px[qubit]
                qz[qubit] ^= qx[qubit]

            def apply_cnot(control, target):
                elimination.__lshift__(CNOT(control, target))
                px[target] ^= px[control]
                pz[control] ^= pz[target]
                qx[target] ^= qx[control]
                qz[control] ^= qz[target]

            for qubit in range(start, num_qubits):
                if px[qubit]:
                    if pz[qubit]:
                        apply_s(qubit)
                    apply_h(qubit)

            pivot = next(
                qubit for qubit in range(start, num_qubits) if pz[qubit]
            )
            if pivot != start:
                apply_cnot(start, pivot)
                apply_cnot(pivot, start)
                apply_cnot(start, pivot)

            for qubit in range(start + 1, num_qubits):
                if pz[qubit]:
                    apply_cnot(qubit, start)

            for qubit in range(start + 1, num_qubits):
                if qx[qubit]:
                    apply_cnot(start, qubit)
                if qz[qubit]:
                    apply_h(qubit)
                    apply_cnot(start, qubit)
                    apply_h(qubit)

            if qz[start]:
                apply_s(start)

        candidate = QProg()
        candidate << elimination.dagger()
        for qubit in range(num_qubits):
            if rng.integers(2):
                candidate << X(qubit)
            if rng.integers(2):
                candidate << Z(qubit)
        return candidate

    circuits = []
    while len(circuits) < n:
        candidate = random_clifford()
        candidate_matrix = unitary(candidate)
        pivot = int(np.argmax(np.abs(candidate_matrix)))
        candidate_phase = np.angle(candidate_matrix.flat[pivot])
        reference_phase = np.angle(reference.flat[pivot])
        if np.allclose(
            candidate_matrix * np.exp(-1j * candidate_phase),
            reference * np.exp(-1j * reference_phase),
            rtol=0.4,
            atol=0.4,
        ):
            circuits.append(candidate)

    return circuits
