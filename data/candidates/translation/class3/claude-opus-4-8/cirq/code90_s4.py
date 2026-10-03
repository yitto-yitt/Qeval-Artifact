# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    qubits = cirq.LineQubit.range(4)
    controls = [qubits[0], qubits[3]]
    targets = [qubits[1], qubits[2]]
    circuit = cirq.Circuit()
    circuit.append(cirq.X(targets[0]).controlled_by(*controls))
    circuit.append(cirq.H(targets[1]).controlled_by(*controls))
    return circuit
