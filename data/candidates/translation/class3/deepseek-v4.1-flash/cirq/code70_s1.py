# EVAL_META: task_id=70, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.CSWAP(q0, q1, q2), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.H(q1), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.ControlledGate(cirq.S**-1).on(q1, q0), strategy=cirq.InsertStrategy.NEW)
    return circuit
