# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    c3h_gate = cirq.ControlledGate(cirq.H, num_controls=2)
    circuit.append(c3h_gate.on(*qubits))
    return circuit
