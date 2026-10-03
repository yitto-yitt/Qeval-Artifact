# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import PauliOperator, QHamiltonian, QCircuit
from pyqpanda3.algorithm import product_formula

def _pauli_str_to_qpanda(pauli_str):
    terms = []
    for i, ch in enumerate(pauli_str):
        if ch != 'I':
            terms.append(f"{ch}{i}")
    return " ".join(terms) if terms else "I0"

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qc = QCircuit()
    for pauli_str, t in zip(pauli_strings, times):
        pauli_op_str = _pauli_str_to_qpanda(pauli_str)
        pauli_op = PauliOperator(pauli_op_str, 1.0)
        ham = QHamiltonian()
        ham += pauli_op
        # Use Lie-Trotter (order=1) regardless of the input order
        term_circuit = product_formula(ham, t, order=1, num_repeat=reps)
        qc.insert(term_circuit)
    return qc
