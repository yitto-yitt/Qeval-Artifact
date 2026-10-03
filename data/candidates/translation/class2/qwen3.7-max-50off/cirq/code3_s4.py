# EVAL_META: task_id=3, framework=cirq, class=2
import cirq

def create_ghz(drawing=False):
    qubits = cirq.LineQubit.range(3)
    ghz = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[0], qubits[2]),
        cirq.measure(*qubits, key='m')
    )
    if drawing:
        return ghz, ghz.to_text_diagram()
    return ghz
