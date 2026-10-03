# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import *
from math import pi

def QFT(n):
    circuit = QCircuit()

    def append_gate(gate):
        circuit << gate

    def append_cp(control_qubit, target_qubit, angle):
        cp_gate = globals().get("CP")
        if cp_gate is not None:
            try:
                append_gate(cp_gate(control_qubit, target_qubit, angle))
                return
            except TypeError:
                pass

        cr_gate = globals().get("CR")
        if cr_gate is not None:
            try:
                append_gate(cr_gate(control_qubit, target_qubit, angle))
                return
            except TypeError:
                pass

        phase_gate = globals().get("P")
        if phase_gate is None:
            phase_gate = globals().get("U1")

        gate = phase_gate(target_qubit, angle)
        controlled_gate = gate.control([control_qubit])
        append_gate(controlled_gate if controlled_gate is not None else gate)

    def swap_registers(num_qubits):
        for qubit in range(num_qubits // 2):
            append_gate(SWAP(qubit, num_qubits - qubit - 1))

    def qft_rotations(num_qubits):
        if num_qubits == 0:
            return
        num_qubits -= 1
        append_gate(H(num_qubits))
        for qubit in range(num_qubits):
            append_cp(qubit, num_qubits, pi / (2 ** (num_qubits - qubit)))
        qft_rotations(num_qubits)

    qft_rotations(n)
    swap_registers(n)
    return circuit
