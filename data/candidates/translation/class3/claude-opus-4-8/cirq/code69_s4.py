# EVAL_META: task_id=69, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[0]))
    circuit.append(cirq.S(q[1]).controlled_by(q[0]))
    circuit.append(cirq.H(q[1]))
    circuit.append((cirq.S**-1)(q[0]).controlled_by(q[1]))
    return circuit
