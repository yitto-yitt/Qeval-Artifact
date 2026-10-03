# EVAL_META: task_id=84, framework=cirq, class=3
import cirq

def controlled_custom_unitary_circuit():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    custom_gate = cirq.ControlledGate(cirq.PhasedXZGate(
        x_exponent=0.3 / cirq.pi,
        z_exponent=(0.2 + 0.1) / cirq.pi,
        axis_phase_exponent=0.1 / cirq.pi
    ))
    circuit.append(custom_gate.on(q0, q1))
    return circuit
