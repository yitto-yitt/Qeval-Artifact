# EVAL_META: task_id=73, framework=cirq, class=3
import cirq


def x_measurement(circuit, qubit, clbit):
    if isinstance(qubit, cirq.Qid):
        target = qubit
    else:
        qubits = sorted(circuit.all_qubits())
        target = qubits[qubit] if qubits else cirq.LineQubit(qubit)
    circuit.append(cirq.H(target))
    circuit.append(cirq.measure(target, key=str(clbit)))
