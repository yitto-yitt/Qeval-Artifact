# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QProg, PauliOperator, VariationalQuantumCircuit, simulate
def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    machine = QuantumMachine()
    qubits = machine.qAlloc_many(n_qubits)
    prog = QProg()
    for pauli_str, t in zip(pauli_strings, times):
        dt = t / reps
        for _ in range(reps):
            op = PauliOperator({pauli_str: 1.0})
            var_circ = VariationalQuantumCircuit()
            var_circ.append_pauli_evolution(op, dt, qubits)
            prog << var_circ
    return prog
