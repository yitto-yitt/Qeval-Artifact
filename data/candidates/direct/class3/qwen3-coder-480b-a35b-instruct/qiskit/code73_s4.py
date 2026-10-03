# EVAL_META: task_id=73, framework=qiskit, class=3
from qiskit import QuantumCircuit


def x_measurement(circuit, qubit, clbit):
    """
    Add an X-basis measurement on qubit at index `qubit`, storing the result to classical bit `clbit`.
    
    Args:
        circuit: QuantumCircuit object
        qubit: qubit index
        clbit: classical bit index
    """
    circuit.h(qubit)
    circuit.measure(qubit, clbit)
    circuit.h(qubit)
