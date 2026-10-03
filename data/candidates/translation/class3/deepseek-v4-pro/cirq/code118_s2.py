# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    gate = cirq.XPowGate(exponent=0.5).controlled(3)
    circuit.append(gate.on(*qubits))
    return circuit
