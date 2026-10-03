# EVAL_META: task_id=36, framework=cirq, class=3
import cirq

def bv_function(s):
    n = len(s)
    qubits = cirq.LineQubit.range(n + 1)
    circuit = cirq.Circuit(cirq.I.on_each(qubits))
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.append(cirq.CNOT(qubits[index], qubits[n]))
    return circuit
