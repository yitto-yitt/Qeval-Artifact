# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    q = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    circuit.append(cirq.ControlledGate(cirq.SX, num_controls=3).on(*q))
    return circuit
