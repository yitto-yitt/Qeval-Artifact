# EVAL_META: task_id=130, framework=cirq, class=3
import cirq

def inv_circuit(n):
    qubits = [cirq.LineQubit(i) for i in range(n)]
    ops = []
    for i in range(2):
        ops.append(cirq.H(qubits[i+1]))
    for i in range(2):
        ops.append(cirq.CNOT(qubits[i+1], qubits[i+2+1]))
    circuit = cirq.Circuit(ops)
    return cirq.inverse(circuit)
