# EVAL_META: task_id=73, framework=cirq, class=3
import cirq

def x_measurement(circuit, qubit, clbit):
    circuit.append(cirq.H(qubit))
    circuit.append(cirq.measure(qubit, key=str(clbit)))
    return circuit
