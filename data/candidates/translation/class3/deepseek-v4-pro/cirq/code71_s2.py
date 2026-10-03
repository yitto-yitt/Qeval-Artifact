# EVAL_META: task_id=71, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_csx01_h1():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append((cirq.X**0.5).controlled(1).on(q0, q1))
    circuit.append(cirq.H(q1))
    return circuit
