# EVAL_META: task_id=71, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_csx01_h1():
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q[0]))
    csx_gate = (cirq.X ** 0.5).controlled(1)
    circuit.append(csx_gate(q[0], q[1]))
    circuit.append(cirq.H(q[1]))
    return circuit
