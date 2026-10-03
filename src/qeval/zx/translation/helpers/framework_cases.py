from __future__ import annotations

from typing import Any


def _type1_cases() -> dict[int, list[dict[str, Any]]]:
    return {
        1: [{"label": "default", "args": ()}],
        14: [{"label": "default", "args": ()}],
        15: [{"label": "default", "args": ()}],
        28: [{"label": "default", "args": ()}],
        31: [{"label": "default", "args": ()}],
        37: [
            {"label": "all_zero", "args": ("0",)},
            {"label": "nontrivial", "args": ("110",)},
        ],
        52: [
            {"label": "bits_00", "args": ("00",)},
            {"label": "bits_01", "args": ("01",)},
            {"label": "bits_10", "args": ("10",)},
            {"label": "bits_11", "args": ("11",)},
        ],
        61: [{"label": "default", "args": ()}],
        64: [
            {"label": "zero_secret", "args": ("00",)},
            {"label": "nontrivial_secret", "args": ("110",)},
        ],
        67: [
            {"label": "alice0_bob0", "args": (0, 0)},
            {"label": "alice0_bob1", "args": (0, 1)},
            {"label": "alice1_bob0", "args": (1, 0)},
            {"label": "alice1_bob1", "args": (1, 1)},
        ],
        77: [
            {"label": "deterministic", "args": ({0: 1.0},)},
            {"label": "nonuniform", "args": ({0: 0.25, 1: 0.75},)},
        ],
        92: [{"label": "default", "args": ()}],
    }


def _type2_cases() -> dict[int, list[dict[str, Any]]]:
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import random_statevector

    def bell_circuit() -> QuantumCircuit:
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        return circuit

    return {
        2: [{"label": "default", "args": ()}],
        3: [{"label": "drawing_false", "args": (False,)}],
        5: [{"label": "default", "args": ()}],
        6: [{"label": "num_qubits_3", "args": (3,)}],
        11: [{"label": "bell_state", "args": (bell_circuit(),)}],
        39: [{"label": "n3", "args": (3,)}],
        62: [
            {"label": "z_one", "args": ([1], [0])},
            {"label": "x_zero", "args": ([0], [1])},
            {"label": "mixed_four_qubits", "args": ([0, 1, 1, 0], [0, 0, 1, 1])},
        ],
        66: [{"label": "default", "args": ()}],
        139: [{"label": "random_state_seed_42_qargs_1", "args": (random_statevector(4, seed=42), [1])}],
    }


def _type3_cases() -> dict[int, list[dict[str, Any]]]:
    from qiskit import QuantumCircuit
    from qiskit.circuit import Parameter
    from qiskit.circuit.library import HGate, XGate
    from qiskit.quantum_info import Operator, random_unitary

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

    def x_measurement_input() -> QuantumCircuit:
        return QuantumCircuit(3, 3)

    def gate_input_circuit() -> QuantumCircuit:
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        return circuit

    return {
        0: [{"label": "n3", "args": (3,)}],
        4: [{"label": "default", "args": ()}],
        7: [{"label": "default", "args": ()}],
        8: [{"label": "unbound", "args": (None,)}, {"label": "value_0_37", "args": (0.37,)}],
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
        73: [{"label": "qubit_2_clbit_1", "args": (x_measurement_input(), 2, 1), "compare_modified_input": 0}],
        78: [{"label": "n3", "args": (3,)}],
        81: [{"label": "default", "args": ()}],
        84: [{"label": "default", "args": ()}],
        86: [{"label": "default", "args": ()}],
        89: [{"label": "default", "args": ()}],
        90: [{"label": "default", "args": ()}],
        99: [{"label": "rx_ry_rz_params", "args": (parameter_removal_circuit(),)}],
        105: [{"label": "default", "args": ()}],
        106: [{"label": "default", "args": ()}],
        108: [{"label": "h_x", "args": (Operator(HGate()), Operator(XGate()))}],
        109: [{"label": "default", "args": ()}],
        110: [{"label": "one_qubit_clifford_n1", "args": (clifford_circuit(), 1), "compare_to_input": 0}],
        112: [{"label": "two_paulis_reps1", "args": (["XI", "IZ"], [0.2, 0.4], 1, 1)}],
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
        147: [{"label": "empty_5q", "args": (QuantumCircuit(5),)}],
    }


def build_cases() -> dict[int, list[dict[str, Any]]]:
    cases: dict[int, list[dict[str, Any]]] = {}
    for group in (_type1_cases(), _type2_cases(), _type3_cases()):
        cases.update(group)
    return cases
