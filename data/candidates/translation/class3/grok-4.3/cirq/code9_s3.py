# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    n = 3
    reps = 1
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    param_idx = 0
    for rep in range(reps + 1):
        for i in range(n):
            qubit = qubits[i]
            for gate_cls in [cirq.Rz, cirq.Ry, cirq.Rz]:
                symbol = sympy.Symbol(f"param_{param_idx}")
                circuit.append(gate_cls(symbol).on(qubit))
                param_idx += 1
        if rep < reps:
            circuit.append(cirq.Barrier(*qubits))
            for j in range(n - 1, 0, -1):
                circuit.append(cirq.CNOT.on(qubits[j], qubits[j - 1]))
            circuit.append(cirq.Barrier(*qubits))
    return circuit
