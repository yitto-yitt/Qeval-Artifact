from __future__ import annotations

from dataclasses import dataclass
from typing import Any


TARGET_QISKIT_VERSIONS = {
    "qiskit": "2.3.1",
    "qiskit-aer": "0.17.2",
    "qiskit-ibm-runtime": "0.46.1",
}

CLASS_ID = 3
TASK_IDS = [
    0,
    4,
    7,
    8,
    9,
    10,
    12,
    13,
    23,
    26,
    27,
    36,
    38,
    41,
    44,
    49,
    50,
    57,
    58,
    59,
    60,
    65,
    69,
    70,
    71,
    73,
    78,
    81,
    84,
    86,
    89,
    90,
    99,
    105,
    106,
    108,
    109,
    110,
    112,
    116,
    117,
    118,
    119,
    120,
    125,
    126,
    130,
    145,
    147,
]


@dataclass(frozen=True)
class TaskSpec:
    task_id: int
    class_id: int
    difficulty: str
    entrypoint: str
    signature: str
    description: str
    return_format: str


def get_task_spec(task_id: int) -> TaskSpec:
    try:
        return TASK_SPECS[task_id]
    except KeyError as exc:
        raise ValueError(f"Unsupported task id: {task_id}") from exc


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


TASK_SPECS: dict[int, TaskSpec] = {
    0: TaskSpec(
        task_id=0,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_quantum_circuit",
        signature="create_quantum_circuit(n_qubits)",
        description="Generate a Quantum Circuit for the given int 'n_qubits' and return it.You must implement this using a function named `create_quantum_circuit` with the following arguments: n_qubits.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    4: TaskSpec(
        task_id=4,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_unitary_from_matrix",
        signature="create_unitary_from_matrix()",
        description="Write the function that converts the matrix [[0, 0, 0, 1],[0, 0, 1, 0],[1, 0, 0, 0],[0, 1, 0, 0]] into a unitary gate and apply it to a Quantum Circuit. Then return the circuit.You must implement this using a function named `create_unitary_from_matrix` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    7: TaskSpec(
        task_id=7,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_parametrized_gate",
        signature="create_parametrized_gate()",
        description="Generate a 1 qubit QuantumCircuit with a parametrized Rx gate with parameter \"theta\". You must implement this using a function named `create_parametrized_gate` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    8: TaskSpec(
        task_id=8,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="rx_gate",
        signature="rx_gate(value)",
        description="Return a 1-qubit QuantumCircuit with a parametrized Rx gate and parameter \"theta\". If value is not None, return the circuit with value assigned to theta. You must implement this using a function named `rx_gate` with the following arguments: value.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    9: TaskSpec(
        task_id=9,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_efficientSU2",
        signature="create_efficientSU2()",
        description="Generate an EfficientSU2 circuit with 3 qubits, 1 reps and make insert_barriers true. You must implement this using a function named `create_efficientSU2` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    10: TaskSpec(
        task_id=10,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_operator",
        signature="create_operator()",
        description="Create a Qiskit circuit with the following unitary [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]], consisting of only single-qubit gates and CX gates, then transpile the circuit using pass manager with optimization level as 1. You must implement this using a function named `create_operator` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    12: TaskSpec(
        task_id=12,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="get_unitary",
        signature="get_unitary()",
        description="Get unitary matrix for a phi plus bell circuit and return it. You must implement this using a function named `get_unitary` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    13: TaskSpec(
        task_id=13,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="custom_rotation_gate",
        signature="custom_rotation_gate()",
        description="Create a quantum circuit that carries out a custom single-qubit rotation gate (U gate) with angles theta, phi and lambda all equal to pi/2. You must implement this using a function named `custom_rotation_gate` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    23: TaskSpec(
        task_id=23,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="dj_constant_oracle",
        signature="dj_constant_oracle()",
        description="Create a constant-one oracle for use in a Deutsch-Jozsa experiment. The oracle takes two input bits (qubits 0 and 1) and writes to one output bit (qubit 2). You must implement this using a function named `dj_constant_oracle` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    26: TaskSpec(
        task_id=26,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="bell_dag",
        signature="bell_dag()",
        description="Construct a DAG circuit for a 3-qubit Quantum Circuit with the bell state applied on qubit 0 and 1. Finally return the DAG Circuit object. You must implement this using a function named `bell_dag` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    27: TaskSpec(
        task_id=27,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="apply_op_back",
        signature="apply_op_back()",
        description="Generate a DAG circuit for 3-qubit Quantum Circuit which consists of H gate on qubit 0 and CX gate on qubit 0 and 1. After converting the circuit to DAG, apply a Hadamard operation to the back of qubit 0 and return the DAGCircuit. You must implement this using a function named `apply_op_back` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    36: TaskSpec(
        task_id=36,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="bv_function",
        signature="bv_function(s)",
        description="Write a function to design a Bernstein-Vazirani oracle from a bitstring and return it. You must implement this using a function named `bv_function` with the following arguments: s.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    38: TaskSpec(
        task_id=38,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_quantum_circuit_based_h0_crz01_h1_cry10",
        signature="create_quantum_circuit_based_h0_crz01_h1_cry10(theta)",
        description="Build a 2-qubit Quantum Circuit composed by H gate in Quantum register 0, Controlled-RZ gate in quantum register 0 1 with given input theta value, H gate in quantum register 1 and Controlled-RY gate in quantum register 1 0 with given input theta value. You must implement this using a function named `create_quantum_circuit_based_h0_crz01_h1_cry10` with the following arguments: theta.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    41: TaskSpec(
        task_id=41,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="compose_op",
        signature="compose_op()",
        description="Compose YX with a 3-qubit identity operator on qubits 0 and 2 using the Operator and the Pauli 'YX' class in Qiskit. Return the operator instance. You must implement this using a function named `compose_op` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    44: TaskSpec(
        task_id=44,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="tensor_circuits",
        signature="tensor_circuits()",
        description="Write an example using Qiskit that performs tensor operation on a 1-qubit quantum circuit with an X gate and a 2-qubit quantum circuit with a CRY gate, where the CRY gate has an angle of 0.2 radians and is controlled by qubit 0. The final circuit should place the 2-qubit CRY circuit before the 1-qubit X circuit in the tensor-product ordering. You must implement this using a function named `tensor_circuits` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    49: TaskSpec(
        task_id=49,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="simple_elitzur_vaidman",
        signature="simple_elitzur_vaidman()",
        description="Return a simple Elitzur Vaidman bomb tester circuit without measurements. You must implement this using a function named `simple_elitzur_vaidman` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    50: TaskSpec(
        task_id=50,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="remove_gate_in_position",
        signature="remove_gate_in_position(circuit, position)",
        description="Remove the gate in the input position for the given Quantum Circuit. You must implement this using a function named `remove_gate_in_position` with the following arguments: circuit, position.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    57: TaskSpec(
        task_id=57,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="create_swap_gate",
        signature="create_swap_gate()",
        description="Design a SWAP gate using only CX gates. You must implement this using a function named `create_swap_gate` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    58: TaskSpec(
        task_id=58,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="create_ch_gate",
        signature="create_ch_gate()",
        description="Design a CH gate using CX and RY gates. You must implement this using a function named `create_ch_gate` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    59: TaskSpec(
        task_id=59,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="create_cz_gate",
        signature="create_cz_gate()",
        description="Design a CZ gate using only H and CNOT gates and return the quantum circuit. You must implement this using a function named `create_cz_gate` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    60: TaskSpec(
        task_id=60,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="create_cy_gate",
        signature="create_cy_gate()",
        description="Design a CY gate using only one CX gate and any other single qubit gates. You must implement this using a function named `create_cy_gate` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    65: TaskSpec(
        task_id=65,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="QFT",
        signature="QFT(n)",
        description="Design a Quantum Fourier Transform circuit for n qubits using basic Quantum gates. You must implement this using a function named `QFT` with the following arguments: n.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    69: TaskSpec(
        task_id=69,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_quantum_circuit_based_h0_cs01_h1_csdg10",
        signature="create_quantum_circuit_based_h0_cs01_h1_csdg10()",
        description="Build a Quantum Circuit composed by the gates H in Quantum register 0, Controlled-S gate in quantum register 0 1, H gate in quantum register 1 and Controlled-S dagger gate in quantum register 1 0. You must implement this using a function named `create_quantum_circuit_based_h0_cs01_h1_csdg10` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    70: TaskSpec(
        task_id=70,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_quantum_circuit_based_h0_cswap012_h1_csdg10",
        signature="create_quantum_circuit_based_h0_cswap012_h1_csdg10()",
        description="Build a Quantum Circuit composed by the gates H in Quantum register 0, Controlled-SWAP gate, also known as the Fredkin gate in quantum register 0 1 2, H gate in quantum register 1 and Controlled-S dagger gate in quantum register 1 0. You must implement this using a function named `create_quantum_circuit_based_h0_cswap012_h1_csdg10` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    71: TaskSpec(
        task_id=71,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_quantum_circuit_based_h0_csx01_h1",
        signature="create_quantum_circuit_based_h0_csx01_h1()",
        description="Build a 3-qubit Quantum Circuit composed by the gates H in Quantum register 0, Controlled-SX gate in quantum register 0 1, and H gate in Quantum register 1. You must implement this using a function named `create_quantum_circuit_based_h0_csx01_h1` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    73: TaskSpec(
        task_id=73,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="x_measurement",
        signature="x_measurement(circuit, qubit, clbit)",
        description="Add an X-basis measurement on qubit at index `qubit`, storing the result to classical bit `clbit`. You must implement this using a function named `x_measurement` with the following arguments: circuit, qubit, clbit.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    78: TaskSpec(
        task_id=78,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="qft_no_swaps",
        signature="qft_no_swaps(num_qubits)",
        description="Return an inverse quantum Fourier transform circuit without the swap gates. You must implement this using a function named `qft_no_swaps` with the following arguments: num_qubits.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    81: TaskSpec(
        task_id=81,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="convert_qasm_string_to_quantum_circuit",
        signature="convert_qasm_string_to_quantum_circuit()",
        description="Generate a QASM 2 string representing a Phi plus Bell state quantum circuit. Then, convert this QASM 2 string into a Quantum Circuit object and return the resulting circuit. You must implement this using a function named `convert_qasm_string_to_quantum_circuit` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    84: TaskSpec(
        task_id=84,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="controlled_custom_unitary_circuit",
        signature="controlled_custom_unitary_circuit()",
        description="Create a 2-qubit quantum circuit where you define a custom 1-qubit unitary gate with angles 0.3, 0.2, and 0.1 and apply it as a controlled gate with qubit 0 as control and qubit 1 as target. Return the final circuit. You must implement this using a function named `controlled_custom_unitary_circuit` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    86: TaskSpec(
        task_id=86,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="collect_linear_blocks_with_and_without_limit",
        signature="collect_linear_blocks_with_and_without_limit()",
        description="Create a 5-qubit quantum circuit with an H gate on qubit 0 followed by a chain of CX gates, and apply Qiskit's CollectLinearFunctions transpiler pass. Return two circuits: 1. One with no block width restriction. 2. One with a max_block_width of 3. Use PassManager to apply the pass and return both circuits. You must implement this using a function named `collect_linear_blocks_with_and_without_limit` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    89: TaskSpec(
        task_id=89,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_controlled_hgate",
        signature="create_controlled_hgate()",
        description="Construct a quantum circuit with a three-qubit controlled-Hadamard gate, using qubit 0 and qubit 1 as the control bits and qubit 2 as the target bit. Return the circuit. You must implement this using a function named `create_controlled_hgate` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    90: TaskSpec(
        task_id=90,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_custom_controlled",
        signature="create_custom_controlled()",
        description="Create a custom 2-qubit gate with an X gate on qubit 0 and an H gate on qubit 1. Then, add two control qubits to this gate. Apply this controlled gate to a 4-qubit circuit, using qubits 0 and 3 as controls and qubits 1 and 2 as targets. Return the final circuit. You must implement this using a function named `create_custom_controlled` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    99: TaskSpec(
        task_id=99,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="remove_unassigned_parameterized_gates",
        signature="remove_unassigned_parameterized_gates(circuit)",
        description="Remove all the gates with unassigned parameters from the given circuit. You must implement this using a function named `remove_unassigned_parameterized_gates` with the following arguments: circuit.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    105: TaskSpec(
        task_id=105,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="initialize_cnot_dihedral",
        signature="initialize_cnot_dihedral()",
        description="Initialize a CNOTDihedral element from a QuantumCircuit consist of 2-qubits with cx gate on qubit 0 and 1 and t gate on qubit 0 and return. You must implement this using a function named `initialize_cnot_dihedral` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    106: TaskSpec(
        task_id=106,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="compose_cnot_dihedral",
        signature="compose_cnot_dihedral()",
        description="Create two Quantum Circuits of 2 qubits. First quantum circuit should have a cx gate on qubits 0 and 1 and a T gate on qubit 0. The second one is the same but with an additional X gate on qubit 1. Convert the two quantum circuits into CNOTDihedral elements and return the composed circuit. You must implement this using a function named `compose_cnot_dihedral` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    108: TaskSpec(
        task_id=108,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="initialize_adjoint_and_compose",
        signature="initialize_adjoint_and_compose(data1, data2)",
        description="Initialize Choi matrices for the given data1 and data2 as inputs. Compute data1 adjoint, and then return the data1 Choi matrix, its adjoint and the composed choi matrices in order. You must implement this using a function named `initialize_adjoint_and_compose` with the following arguments: data1, data2.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    109: TaskSpec(
        task_id=109,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="circuit",
        signature="circuit()",
        description="Create a parameterized quantum circuit using minimum resources whose statevector output cover the equatorial plane of the surface of the bloch sphere. You must implement this using a function named `circuit` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    110: TaskSpec(
        task_id=110,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="equivalent_clifford_circuit",
        signature="equivalent_clifford_circuit(circuit, n)",
        description="Given a clifford circuit return a list of n random clifford circuits which are equivalent to the given circuit up to a relative and absolute tolerance of 0.4. You must implement this using a function named `equivalent_clifford_circuit` with the following arguments: circuit, n.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    112: TaskSpec(
        task_id=112,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="create_product_formula_circuit",
        signature="create_product_formula_circuit(pauli_strings, times, order, reps)",
        description="Create a quantum circuit using LieTrotter for a list of Pauli strings and times. Each Pauli string is associated with a corresponding time in the 'times' list. The function should return the resulting QuantumCircuit. You must implement this using a function named `create_product_formula_circuit` with the following arguments: pauli_strings, times, order, reps.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    116: TaskSpec(
        task_id=116,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="synthesize_evolution_gate",
        signature="synthesize_evolution_gate(pauli_string, time)",
        description="Synthesize an evolution gate using MatrixExponential for a given Pauli string and time. The Pauli string can be any combination of 'I', 'X', 'Y', and 'Z'. Return the resulting QuantumCircuit. You must implement this using a function named `synthesize_evolution_gate` with the following arguments: pauli_string, time.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    117: TaskSpec(
        task_id=117,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="decompose_unitary",
        signature="decompose_unitary(unitary)",
        description="Decompose a 4x4 unitary using the TwoQubitBasisDecomposer with CXGate as the basis gate.Return the resulting QuantumCircuit. You must implement this using a function named `decompose_unitary` with the following arguments: unitary.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    118: TaskSpec(
        task_id=118,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="create_c3sx_circuit",
        signature="create_c3sx_circuit()",
        description="Create a QuantumCircuit with a C3SXGate applied to the first four qubits. You must implement this using a function named `create_c3sx_circuit` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    119: TaskSpec(
        task_id=119,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="create_ripple_carry_adder_circuit",
        signature="create_ripple_carry_adder_circuit(num_state_qubits, kind)",
        description="Create a QuantumCircuit with a CDKMRippleCarryAdder applied to the qubits. The kind of adder can be 'full', 'half', or 'fixed'. You must implement this using a function named `create_ripple_carry_adder_circuit` with the following arguments: num_state_qubits, kind.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    120: TaskSpec(
        task_id=120,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="create_diagonal_circuit",
        signature="create_diagonal_circuit(diag)",
        description="Create a QuantumCircuit with a Diagonal gate applied to the qubits.The diagonal elements are provided in the list 'diag'. You must implement this using a function named `create_diagonal_circuit` with the following arguments: diag.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    125: TaskSpec(
        task_id=125,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="circ_to_gate",
        signature="circ_to_gate(circ)",
        description="Given a QuantumCircuit, convert it into a gate equivalent to the action of the input circuit and return it. You must implement this using a function named `circ_to_gate` with the following arguments: circ.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    126: TaskSpec(
        task_id=126,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="calculate_phase_difference_fidelity",
        signature="calculate_phase_difference_fidelity()",
        description="Create two quantum operators using Hadamard gate that differ only by a global phase. Calculate the process fidelity between these two operators and return the process fidelity value. You must implement this using a function named `calculate_phase_difference_fidelity` with no arguments.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    130: TaskSpec(
        task_id=130,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="inv_circuit",
        signature="inv_circuit(n)",
        description="Create a quantum circuit with 'n' qubits. Apply Hadamard gates to the second and third qubits. Then apply CNOT gates between the second and fourth qubits, and between the third and fifth qubits. Finally give the inverse of the quantum circuit. You must implement this using a function named `inv_circuit` with the following arguments: n.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    145: TaskSpec(
        task_id=145,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="qft_inverse",
        signature="qft_inverse(n)",
        description="Return the inverse qft circuit for n qubits. You must implement this using a function named `qft_inverse` with the following arguments: n.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
    147: TaskSpec(
        task_id=147,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="mcy",
        signature="mcy(qc)",
        description="Add a multi-controlled-Y operation to qubit 4, controlled by qubits 0-3. You must implement this using a function named `mcy` with the following arguments: qc.",
        return_format="Return only the requested Qiskit object or sequence of Qiskit objects.",
    ),
}
