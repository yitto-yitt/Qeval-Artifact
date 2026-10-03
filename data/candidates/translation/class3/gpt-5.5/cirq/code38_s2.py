# EVAL_META: task_id=38, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[0]))
    circuit.append(cirq.rz(theta).controlled().on(q[0], q[1]))
    circuit.append(cirq.H(q[1]))
    circuit.append(cirq.ry(theta).controlled().on(q[1], q[0]))
    return circuit
