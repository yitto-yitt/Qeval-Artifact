from __future__ import annotations

from typing import Any


def build_cases() -> dict[int, list[dict[str, Any]]]:
    from qiskit import QuantumCircuit
    from qiskit.circuit import Parameter
    from qiskit.circuit.library import HGate, XGate
    from qiskit.quantum_info import Operator
    from qiskit.quantum_info import random_unitary

    def removal_circuit() -> QuantumCircuit:
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.x(1)
        return circuit

    def parameter_removal_circuit() -> QuantumCircuit:
        theta = Parameter("theta")
        phi = Parameter("phi")
        circuit = QuantumCircuit(1)
        circuit.rx(theta, 0)
        circuit.ry(0.2, 0)
        circuit.rz(phi, 0)
        return circuit

    def clifford_circuit() -> QuantumCircuit:
        circuit = QuantumCircuit(1)
        circuit.h(0)
        circuit.s(0)
        return circuit

    def mcy_input() -> QuantumCircuit:
        return QuantumCircuit(5)

    def x_measurement_input() -> QuantumCircuit:
        return QuantumCircuit(3, 3)

    def choi_data() -> tuple[Operator, Operator]:
        return Operator(HGate()), Operator(XGate())

    def gate_input_circuit() -> QuantumCircuit:
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        return circuit

    return {
        0: [{"label": "n3", "args": (3,)}],
        4: [{"label": "default", "args": ()}],
        7: [{"label": "default", "args": ()}],
        8: [
            {"label": "unbound", "args": (None,)},
            {"label": "value_0_37", "args": (0.37,)},
        ],
        9: [{"label": "default", "args": ()}],
        10: [{"label": "default", "args": ()}],
        12: [{"label": "default", "args": ()}],
        13: [{"label": "default", "args": ()}],
        23: [{"label": "default", "args": ()}],
        26: [{"label": "default", "args": ()}],
        27: [{"label": "default", "args": ()}],
        36: [{"label": "s_110", "args": ("110",)}],
        38: [{"label": "theta_0_37", "args": (0.37,)}],
        41: [{"label": "default", "args": ()}],
        44: [{"label": "default", "args": ()}],
        49: [{"label": "default", "args": ()}],
        50: [{"label": "remove_position_1", "args": (removal_circuit(), 1)}],
        57: [{"label": "default", "args": ()}],
        58: [{"label": "default", "args": ()}],
        59: [{"label": "default", "args": ()}],
        60: [{"label": "default", "args": ()}],
        65: [{"label": "n3", "args": (3,)}],
        69: [{"label": "default", "args": ()}],
        70: [{"label": "default", "args": ()}],
        71: [{"label": "default", "args": ()}],
        73: [
            {
                "label": "qubit_2_clbit_1",
                "args": (x_measurement_input(), 2, 1),
                "compare_modified_input": 0,
            }
        ],
        78: [{"label": "n3", "args": (3,)}],
        81: [{"label": "default", "args": ()}],
        84: [{"label": "default", "args": ()}],
        86: [{"label": "default", "args": ()}],
        89: [{"label": "default", "args": ()}],
        90: [{"label": "default", "args": ()}],
        99: [{"label": "rx_ry_rz_params", "args": (parameter_removal_circuit(),)}],
        105: [{"label": "default", "args": ()}],
        106: [{"label": "default", "args": ()}],
        108: [{"label": "h_x", "args": choi_data()}],
        109: [{"label": "default", "args": ()}],
        110: [{"label": "one_qubit_clifford_n1", "args": (clifford_circuit(), 1), "compare_to_input": 0}],
        112: [
            {
                "label": "two_paulis_reps1",
                "args": (["XI", "IZ"], [0.2, 0.4], 1, 1),
            }
        ],
        116: [{"label": "XI_time_0_4", "args": ("XI", 0.4)}],
        117: [{"label": "random_unitary_seed_17", "args": (random_unitary(4, seed=17),)}],
        118: [{"label": "default", "args": ()}],
        119: [
            {"label": "kind_full", "args": (2, "full")},
            {"label": "kind_half", "args": (2, "half")},
            {"label": "kind_fixed", "args": (2, "fixed")},
        ],
        120: [{"label": "diag_pm_i", "args": ([1, -1, 1j, -1j],)}],
        125: [{"label": "h_cx", "args": (gate_input_circuit(),)}],
        126: [{"label": "default", "args": ()}],
        130: [{"label": "n5", "args": (5,)}],
        145: [{"label": "n3", "args": (3,)}],
        147: [{"label": "empty_5q", "args": (mcy_input(),)}],
    }
