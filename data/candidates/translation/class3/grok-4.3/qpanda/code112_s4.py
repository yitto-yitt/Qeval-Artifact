# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import *
from pyqpanda3.core import PauliOperator

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    machine = CPUQVM()
    machine.init_qvm()
    qlist = machine.qAlloc_many(n_qubits)
    prog = QProg()
    for pauli_str, t in zip(pauli_strings, times):
        h = PauliOperator(pauli_str, t)
        for _ in range(reps):
            prog.insert(simulate_hamiltonian(qlist, h, 1.0/reps, 1))
    return prog
