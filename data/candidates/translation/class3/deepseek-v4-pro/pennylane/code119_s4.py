# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    ops = []

    if kind == 'full':
        c_in = 0
        a_wires = [2*i + 1 for i in range(n)]
        b_wires = [2*i + 2 for i in range(n)]
        c_out = 2*n + 1
        target_wires = b_wires + [c_out]
        target_size = n + 1
        controls = [(c_in, 1)] + [(a_wires[i], 1 << i) for i in range(n)]
    elif kind == 'half':
        a_wires = [2*i for i in range(n)]
        b_wires = [2*i + 1 for i in range(n)]
        c_out = 2*n
        target_wires = b_wires + [c_out]
        target_size = n + 1
        controls = [(a_wires[i], 1 << i) for i in range(n)]
    elif kind == 'fixed':
        a_wires = [2*i for i in range(n)]
        b_wires = [2*i + 1 for i in range(n)]
        target_wires = b_wires
        target_size = n
        controls = [(a_wires[i], 1 << i) for i in range(n)]
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    ops.append(qml.QFT(wires=target_wires))

    for ctrl, weight in controls:
        for j, t in enumerate(target_wires):
            phase = 2 * np.pi * weight * (1 << j) / (1 << target_size)
            if not np.isclose(phase % (2 * np.pi), 0.0):
                ops.append(qml.ControlledPhaseShift(phase, control_wires=ctrl, wires=t))

    ops.append(qml.adjoint(qml.QFT)(wires=target_wires))

    return qml.tape.QuantumScript(ops)