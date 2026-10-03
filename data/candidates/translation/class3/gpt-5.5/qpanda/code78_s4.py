# EVAL_META: task_id=78, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def qft_no_swaps(num_qubits):
    circuit = pq.QCircuit()

    def append_cp(ctrl, targ, theta):
        cp_gate = getattr(pq, "CP", None)
        if cp_gate is not None:
            try:
                circuit << cp_gate(ctrl, targ, theta)
                return
            except TypeError:
                pass

        phase_gate = getattr(pq, "P", None)
        if phase_gate is None:
            phase_gate = getattr(pq, "U1", None)

        if phase_gate is not None:
            circuit << phase_gate(ctrl, theta / 2.0)
            circuit << pq.CNOT(ctrl, targ)
            circuit << phase_gate(targ, -theta / 2.0)
            circuit << pq.CNOT(ctrl, targ)
            circuit << phase_gate(targ, theta / 2.0)
        else:
            circuit << pq.RZ(ctrl, theta / 2.0)
            circuit << pq.CNOT(ctrl, targ)
            circuit << pq.RZ(targ, -theta / 2.0)
            circuit << pq.CNOT(ctrl, targ)
            circuit << pq.RZ(targ, theta / 2.0)

    if num_qubits <= 0:
        return circuit

    circuit << pq.H(0)
    for target in range(1, num_qubits):
        for control in range(target - 1, -1, -1):
            append_cp(control, target, -math.pi / (2 ** (target - control)))
        circuit << pq.H(target)

    return circuit
