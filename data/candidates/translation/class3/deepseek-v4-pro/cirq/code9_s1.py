# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import sympy

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    params = [sympy.Symbol(f'p{i}') for i in range(6)]
    circuit = cirq.Circuit()
    # single-qubit layer
    for i, q in enumerate(qubits):
        circuit.append(cirq.ry(params[2*i])(q))
        circuit.append(cirq.rz(params[2*i+1])(q))
    # entangling layer (full entanglement)
    pairs = [(0, 1), (0, 2), (1, 2)]
    for c, t in pairs:
        circuit.append(cirq.CNOT(qubits[c], qubits[t]))
    return circuit
