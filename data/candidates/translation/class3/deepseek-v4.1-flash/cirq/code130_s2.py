# EVAL_META: task_id=130, framework=cirq, class=3
import cirq

def inv_circuit(n):
    qubits = cirq.LineQubit.range(n)
    qc = cirq.Circuit()
    for i in range(2):
        qc.append(cirq.H(qubits[i + 1]))
    for i in range(2):
        qc.append(cirq.CNOT(qubits[i + 1], qubits[i + 3]))
    return cirq.inverse(qc)
