# EVAL_META: task_id=73, framework=cirq, class=3
import cirq


def x_measurement(circuit, qubit, clbit):
    target = qubit if isinstance(qubit, cirq.Qid) else sorted(circuit.all_qubits())[qubit]
    circuit.append(cirq.H(target))
    circuit.append(cirq.measure(target, key=str(clbit)))
