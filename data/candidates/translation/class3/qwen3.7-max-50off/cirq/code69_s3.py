# EVAL_META: task_id=69, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.S(q1).controlled_by(q0))
    circuit.append(cirq.H(q1))
    circuit.append((cirq.S**-1)(q0).controlled_by(q1))
    return circuit
