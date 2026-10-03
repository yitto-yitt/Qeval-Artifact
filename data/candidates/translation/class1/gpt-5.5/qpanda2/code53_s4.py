# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def xor_gate(a, b):
    n = 8
    shots = 1024
    a = int(a)
    b = int(b)

    def _run_with_x_indices(indices, shot_count):
        qvm = pq.CPUQVM()
        qvm.init_qvm()
        qubits = qvm.qAlloc_many(n)
        cbits = qvm.cAlloc_many(n)
        prog = pq.QProg()
        for idx in indices:
            prog << pq.X(qubits[idx])
        prog << pq.measure_all(qubits, cbits)
        counts = qvm.run_with_configuration(prog, cbits, shot_count)
        qvm.finalize()
        return dict(counts)

    if not hasattr(xor_gate, "_qpanda_qubit_positions"):
        positions = [0] * n
        for i in range(n):
            calibration_counts = _run_with_x_indices([i], 1)
            key = str(max(calibration_counts, key=calibration_counts.get))
            if len(key) < n:
                key = key.zfill(n)
            positions[i] = key.index("1")
        xor_gate._qpanda_qubit_positions = tuple(positions)

    x_indices = []
    for i in range(n):
        if (a >> i) & 1:
            x_indices.append(i)
    for i in range(n):
        if (b >> i) & 1:
            x_indices.append(i)

    counts = _run_with_x_indices(x_indices, shots)
    positions = xor_gate._qpanda_qubit_positions

    converted_counts = {}
    for key, value in counts.items():
        key = str(key)
        if len(key) < n:
            key = key.zfill(n)
        out_bits = ["0"] * n
        for qubit_index, key_position in enumerate(positions):
            out_bits[n - 1 - qubit_index] = key[key_position]
        out_key = "".join(out_bits)
        converted_counts[out_key] = converted_counts.get(out_key, 0) + value

    total = builtins.sum(converted_counts.values())
    return {key: value / total for key, value in converted_counts.items()}
