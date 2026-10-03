# EVAL_META: task_id=9, framework=cirq, class=3
import cirq

def create_efficientSU2():
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    for qubit in q:
        circuit.append(cirq.ry(cirq.Symbol(f"θ0_{qubit.x}"))(qubit))
        circuit.append(cirq.rz(cirq.Symbol(f"φ0_{qubit.x}"))(qubit))
    circuit.append(cirq.Moment())  # barrier
    for i in range(2):
        circuit.append(cirq.CX(q[i], q[i + 1]))
    circuit.append(cirq.Moment())  # barrier
    for qubit in q:
        circuit.append(cirq.ry(cirq.Symbol(f"θ1_{qubit.x}"))(qubit))
        circuit.append(cirq.rz(cirq.Symbol(f"φ1_{qubit.x}"))(qubit))
    return circuit
