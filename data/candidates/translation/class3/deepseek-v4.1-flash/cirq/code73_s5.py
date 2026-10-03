# EVAL_META: task_id=73, framework=cirq, class=3
import cirq

def x_measurement(circuit, qubit, clbit):
    q = cirq.LineQubit(qubit) if isinstance(qubit, int) else qubit
    key = str(clbit) if isinstance(clbit, int) else clbit
    circuit.append(cirq.H(q))
    circuit.append(cirq.measure(q, key=key))
