# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    qc = cirq.Circuit()
    qc.append(cirq.H(qubits[0]))
    qc.append(cirq.CNOT(qubits[0], qubits[1]))
    qc.append(cirq.CNOT(qubits[1], qubits[2]))
    qc.append(cirq.CNOT(qubits[2], qubits[3]))
    qc.append(cirq.CNOT(qubits[3], qubits[4]))
    pm_full = cirq.Circuit(qc)
    pm_limited = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4])
    )
    return pm_full, pm_limited
