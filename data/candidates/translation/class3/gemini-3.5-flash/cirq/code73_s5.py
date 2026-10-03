# EVAL_META: task_id=73, framework=cirq, class=3
import cirq

def x_measurement(circuit, qubit, clbit):
    q = cirq.LineQubit(qubit) if isinstance(qubit, int) else qubit
    circuit.append(cirq.H(q))
    circuit.append(cirq.measure(q, key=str(clbit)))
    return circuit
