# EVAL_META: task_id=56, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def not_gate(a):
    def _calibrate_positions():
        positions = [None] * 8
        for idx in range(8):
            qvm = pq.CPUQVM()
            qvm.init_qvm()
            try:
                qubits = qvm.qAlloc_many(8)
                cbits = qvm.cAlloc_many(8)
                prog = pq.QProg()
                prog << pq.X(qubits[idx])
                for j in range(8):
                    prog << pq.Measure(qubits[j], cbits[j])
                counts = qvm.run_with_configuration(prog, cbits, 1)
            finally:
                qvm.finalize()
            key = max(counts, key=counts.get)
            positions[idx] = key.index("1")
        return positions

    if not hasattr(not_gate, "_positions"):
        not_gate._positions = _calibrate_positions()

    positions = not_gate._positions
    a_bits = format(a, "08b")
    desired = "".join("1" if a_bits[i] == "0" else "0" for i in range(8))

    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        qubits = qvm.qAlloc_many(8)
        cbits = qvm.cAlloc_many(8)
        prog = pq.QProg()

        for qubit_index, output_pos in enumerate(positions):
            if desired[output_pos] == "1":
                prog << pq.X(qubits[qubit_index])

        for i in range(8):
            prog << pq.Measure(qubits[i], cbits[i])

        shots = 1024
        counts = qvm.run_with_configuration(prog, cbits, shots)
    finally:
        qvm.finalize()

    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
