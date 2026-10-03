# EVAL_META: task_id=3, framework=cirq, class=2
import cirq

def create_ghz(drawing=False):
    qubits = cirq.LineQubit.range(3)
    ghz = cirq.Circuit()
    ghz.append(cirq.H(qubits[0]))
    ghz.append(cirq.CNOT(qubits[0], qubits[1]))
    ghz.append(cirq.CNOT(qubits[0], qubits[2]))
    ghz.append(cirq.measure(*qubits, key='m'))
    if drawing:
        return ghz, None
    return ghz
