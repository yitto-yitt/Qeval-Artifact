from __future__ import annotations

from dataclasses import dataclass
from typing import Any


TARGET_QISKIT_VERSIONS = {
    "qiskit": "2.3.1",
    "qiskit-aer": "0.17.2",
    "qiskit-ibm-runtime": "0.46.1",
}

CLASS_ID = 1
TASK_IDS = [1, 14, 15, 24, 28, 31, 37, 40, 47, 52, 53, 54, 55, 56, 61, 64, 67, 68, 77, 92]


@dataclass(frozen=True)
class TaskSpec:
    task_id: int
    class_id: int
    difficulty: str
    entrypoint: str
    signature: str
    description: str
    return_format: str


TASK_SPECS: dict[int, TaskSpec] = {
    1: TaskSpec(
        task_id=1,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="run_bell_state_simulator",
        signature="run_bell_state_simulator()",
        description=(
            "Define a phi plus Bell state using Qiskit, transpile the circuit with a "
            "preset pass manager at optimization level 1, run it with Qiskit Runtime "
            "Sampler on an Aer simulator backend, and return the measurement result."
        ),
        return_format="Return a probability distribution dict keyed by measurement bitstrings.",
    ),
    14: TaskSpec(
        task_id=14,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="bell_each_shot",
        signature="bell_each_shot()",
        description=(
            "Run a phi plus Bell circuit using Qiskit Runtime Sampler with the Aer "
            "simulator backend for 10 shots. Transpile the circuit with a preset pass "
            "manager at optimization level 1."
        ),
        return_format="Return a probability distribution dict keyed by measurement bitstrings.",
    ),
    15: TaskSpec(
        task_id=15,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="noisy_bell",
        signature="noisy_bell()",
        description=(
            "Transpile a Bell circuit using a preset pass manager at optimization level 1, "
            "run it with Qiskit Runtime Sampler on an Aer simulator created from a fake "
            "backend, and return the execution result."
        ),
        return_format="Return a probability distribution dict keyed by measurement bitstrings.",
    ),
    24: TaskSpec(
        task_id=24,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="dj_algorithm",
        signature="dj_algorithm(oracle)",
        description=(
            "Given a Deutsch-Jozsa oracle where the final qubit is the output qubit, build "
            "and run the Deutsch-Jozsa routine."
        ),
        return_format=(
            "Return a probability distribution dict for the measured input-register "
            "bitstrings. This overrides the original True/False wording."
        ),
    ),
    28: TaskSpec(
        task_id=28,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="visualize_bell_states",
        signature="visualize_bell_states()",
        description="Prepare phi plus and phi minus Bell states and sample their measurement results.",
        return_format=(
            "Return a nested dict with exactly the keys 'phi_plus' and 'phi_minus'. "
            "Each value must be a probability distribution dict keyed by bitstrings. "
            "Do not return a matplotlib histogram object."
        ),
    ),
    31: TaskSpec(
        task_id=31,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="sampler_qiskit",
        signature="sampler_qiskit()",
        description=(
            "Run a Bell circuit on Qiskit Runtime Sampler using an Aer simulator with "
            "the simulator seed set to 42."
        ),
        return_format="Return a probability distribution dict keyed by measurement bitstrings.",
    ),
    37: TaskSpec(
        task_id=37,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="bv_algorithm",
        signature="bv_algorithm(s)",
        description=(
            "Illustrate a Bernstein-Vazirani algorithm routine on Qiskit and run it using "
            "Qiskit Sampler with an Aer simulator backend for a string of 0s and 1s."
        ),
        return_format="Return [bitstrings, result], where bitstrings are the measured input-register bitstrings.",
    ),
    40: TaskSpec(
        task_id=40,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="init_random_3qubit",
        signature="init_random_3qubit(desired_vector)",
        description=(
            "Initialize a non-trivial 3-qubit state from the given desired vector and "
            "sample it using Qiskit Runtime Sampler on an Aer simulator backend."
        ),
        return_format="Return a probability distribution dict keyed by measurement bitstrings.",
    ),
    47: TaskSpec(
        task_id=47,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="random_coin_flip",
        signature="random_coin_flip(samples)",
        description=(
            "Design a one-qubit quantum coin flip routine using a Hadamard gate and sample "
            "it for the requested number of shots."
        ),
        return_format=(
            "Return a probability distribution dict with exactly the keys 'Heads' and "
            "'Tails', and values that sum to 1.0."
        ),
    ),
    52: TaskSpec(
        task_id=52,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="send_bits",
        signature="send_bits(bitstring)",
        description=(
            "Provide a quantum circuit for transmitting two classical bits through one "
            "qubit of quantum communication when sender and receiver share entanglement."
        ),
        return_format="Return a QuantumCircuit only.",
    ),
    53: TaskSpec(
        task_id=53,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="xor_gate",
        signature="xor_gate(a, b)",
        description=(
            "Given two 8-bit integers a and b, design a quantum circuit that acts as a "
            "classical XOR gate and sample the output."
        ),
        return_format="Return a probability distribution dict keyed by 8-bit measurement strings.",
    ),
    54: TaskSpec(
        task_id=54,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="and_gate",
        signature="and_gate(a, b)",
        description=(
            "Given two 3-bit integers a and b, design a quantum circuit that acts as a "
            "bitwise classical AND gate and sample the output."
        ),
        return_format="Return a probability distribution dict keyed by 3-bit measurement strings.",
    ),
    55: TaskSpec(
        task_id=55,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="or_gate",
        signature="or_gate(a, b)",
        description=(
            "Given two 3-bit integers a and b, design a quantum circuit that acts as a "
            "bitwise classical OR gate and sample the output."
        ),
        return_format="Return a probability distribution dict keyed by 3-bit measurement strings.",
    ),
    56: TaskSpec(
        task_id=56,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="not_gate",
        signature="not_gate(a)",
        description=(
            "Given an 8-bit integer a, design a quantum circuit that acts as a classical "
            "bitwise NOT gate and sample the output."
        ),
        return_format="Return a probability distribution dict keyed by 8-bit measurement strings.",
    ),
    61: TaskSpec(
        task_id=61,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_quantum_circuit_with_one_qubit_and_measure",
        signature="create_quantum_circuit_with_one_qubit_and_measure()",
        description=(
            "Build a QuantumCircuit by first creating one Quantum Register and one "
            "Classical Register and then performing measurement on it."
        ),
        return_format="Return a QuantumCircuit only.",
    ),
    64: TaskSpec(
        task_id=64,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="simons_algorithm",
        signature="simons_algorithm(s)",
        description=(
            "Write a function that takes the bitstring 's' as the input and builds a Quantum Circuit such that the output when xor-ed with the input 's' is same as the 's'. When building the quantum circuit make sure the classical registers is named 'c'."
            "You must implement this using a function named `simons_algorithm` with the following arguments: s."
        ),
        return_format="Return a QuantumCircuit only.",
    ),
    67: TaskSpec(
        task_id=67,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="chsh_circuit",
        signature="chsh_circuit(alice, bob)",
        description=(
            "Design a CHSH circuit that takes Alice and Bob input bits and returns the "
            "measured QuantumCircuit."
        ),
        return_format="Return a QuantumCircuit only.",
    ),
    68: TaskSpec(
        task_id=68,
        class_id=CLASS_ID,
        difficulty="difficult",
        entrypoint="zeno_elitzur_vaidman_bomb_tester",
        signature="zeno_elitzur_vaidman_bomb_tester(bomb_live)",
        description=(
            "Design a Zeno Elitzur-Vaidman bomb tester routine using 25 cycles and report "
            "the probabilities of successful live-bomb predictions, dud-bomb predictions, "
            "and detonations."
        ),
        return_format=(
            "Return a probability distribution dict with exactly the keys "
            "'live_predictions', 'dud_predictions', and 'detonations'."
        ),
    ),
    77: TaskSpec(
        task_id=77,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="circuit_from_probability_dist",
        signature="circuit_from_probability_dist(probability_dist)",
        description=(
            "Given a distribution dictionary of the form {measurement: probability}, "
            "return a quantum circuit that produces that distribution."
        ),
        return_format="Return a QuantumCircuit only.",
    ),
    92: TaskSpec(
        task_id=92,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="calculate_stabilizer_state_info",
        signature="calculate_stabilizer_state_info()",
        description=(
            "Construct a Phi plus Bell state quantum circuit and compute the stabilizer "
            "state measurement probabilities."
        ),
        return_format=(
            "Return only the stabilizer-state probability distribution dict. Do not return "
            "the StabilizerState object."
        ),
    ),
}


def get_task_spec(task_id: int) -> TaskSpec:
    try:
        return TASK_SPECS[task_id]
    except KeyError as exc:
        raise ValueError(f"Unsupported task id: {task_id}") from exc


def constant_oracle() -> Any:
    from qiskit import QuantumCircuit

    return QuantumCircuit(3)


def balanced_oracle() -> Any:
    from qiskit import QuantumCircuit

    circuit = QuantumCircuit(3)
    circuit.cx(0, 2)
    circuit.cx(1, 2)
    return circuit


DESIRED_VECTOR = [
    0.5,
    0.0,
    0.0,
    0.5,
    0.0,
    0.5,
    0.5,
    0.0,
]


def build_cases() -> dict[int, list[dict[str, Any]]]:
    return {
        1: [{"label": "default", "args": (), "repeat": 8}],
        14: [{"label": "default", "args": (), "repeat": 400}],
        15: [{"label": "default", "args": (), "repeat": 8}],
        24: [
            {"label": "constant_oracle", "args": (constant_oracle(),)},
            {"label": "balanced_oracle", "args": (balanced_oracle(),)},
        ],
        28: [{"label": "default", "args": (), "repeat": 4}],
        31: [{"label": "default", "args": ()}],
        37: [
            {"label": "all_zero", "args": ("0",), "repeat": 128},
            {"label": "nontrivial", "args": ("110",), "repeat": 128},
        ],
        40: [{"label": "fixed_normalized_vector", "args": (DESIRED_VECTOR,)}],
        47: [{"label": "samples_1024", "args": (1024,), "repeat": 4}],
        52: [
            {"label": "bits_00", "args": ("00",)},
            {"label": "bits_01", "args": ("01",)},
            {"label": "bits_10", "args": ("10",)},
            {"label": "bits_11", "args": ("11",)},
        ],
        53: [
            {"label": "a0_b0", "args": (0, 0)},
            {"label": "a0_b7", "args": (0, 7)},
            {"label": "a3_b5", "args": (3, 5)},
            {"label": "a7_b7", "args": (7, 7)},
        ],
        54: [
            {"label": "a0_b0", "args": (0, 0)},
            {"label": "a0_b7", "args": (0, 7)},
            {"label": "a3_b5", "args": (3, 5)},
            {"label": "a7_b7", "args": (7, 7)},
        ],
        55: [
            {"label": "a0_b0", "args": (0, 0)},
            {"label": "a0_b7", "args": (0, 7)},
            {"label": "a3_b5", "args": (3, 5)},
            {"label": "a7_b7", "args": (7, 7)},
        ],
        56: [
            {"label": "a0", "args": (0,)},
            {"label": "a1", "args": (1,)},
            {"label": "a3", "args": (3,)},
            {"label": "a7", "args": (7,)},
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
        68: [
            {"label": "bomb_live_false", "args": (False,), "repeat": 4},
            {"label": "bomb_live_true", "args": (True,), "repeat": 4},
        ],
        77: [
            {"label": "deterministic", "args": ({0: 1.0},)},
            {"label": "nonuniform", "args": ({0: 0.25, 1: 0.25, 2: 0.5},)},
        ],
        92: [{"label": "default", "args": ()}],
    }
