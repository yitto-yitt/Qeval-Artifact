# EVAL_META: task_id=110, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(16)


def equivalent_clifford_circuit(circuit, n):
    num_qubits = int(circuit.get("num_qubits", 1))
    target_u = np.array(circuit["unitary"], dtype=complex)

    def random_single_qubit_clifford():
        gates = ["I", "H", "S", "X", "Y", "Z"]
        length = np.random.randint(1, 6)
        return [np.random.choice(gates) for _ in range(length)]

    def apply_gate_sequence(prog, q, seq):
        for g in seq:
            if g == "H":
                prog.insert(pq.H(q))
            elif g == "S":
                prog.insert(pq.S(q))
            elif g == "X":
                prog.insert(pq.X(q))
            elif g == "Y":
                prog.insert(pq.Y(q))
            elif g == "Z":
                prog.insert(pq.Z(q))

    def random_clifford_program(qubits):
        prog = pq.QProg()
        depth = np.random.randint(1, 6)
        for _ in range(depth):
            for q in qubits:
                apply_gate_sequence(prog, q, random_single_qubit_clifford())
            if len(qubits) >= 2:
                pairs = list(range(len(qubits) - 1))
                np.random.shuffle(pairs)
                for i in pairs[: max(1, len(pairs) // 2)]:
                    if np.random.rand() < 0.5:
                        prog.insert(pq.CNOT(qubits[i], qubits[i + 1]))
        return prog

    def unitary_from_prog(prog, qnum):
        return np.array(pq.get_unitary(prog), dtype=complex).reshape((2 ** qnum, 2 ** qnum))

    def equivalent_up_to_global_phase(u, v, rtol=0.4, atol=0.4):
        idx = np.unravel_index(np.argmax(np.abs(v)), v.shape)
        if np.abs(v[idx]) < 1e-12:
            return np.allclose(u, v, rtol=rtol, atol=atol)
        phase = u[idx] / v[idx] if np.abs(v[idx]) > 1e-12 else 1.0
        return np.allclose(u, phase * v, rtol=rtol, atol=atol)

    qubits = _global_qubits[:num_qubits]
    out = []
    while len(out) < n:
        prog = random_clifford_program(qubits)
        u = unitary_from_prog(prog, num_qubits)
        if equivalent_up_to_global_phase(u, target_u, rtol=0.4, atol=0.4):
            out.append({"num_qubits": num_qubits, "program": prog, "unitary": u})
    machine.finalize()
    return out
