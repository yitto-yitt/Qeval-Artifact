# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, init_quantum_machine, QMachineType, destroy_quantum_machine
from pyqpanda3.core import PauliOperator, simulate_hamiltonian


def create_product_formula_circuit(pauli_strings, times, order, reps):
    machine = init_quantum_machine(QMachineType.CPU)
    n_qubits = len(pauli_strings[0]) if pauli_strings else 0
    q = machine.qAlloc_many(n_qubits)

    circuit = QCircuit()
    for pauli_string, t in zip(pauli_strings, times):
        term = {}
        for i, p in enumerate(pauli_string):
            if p != 'I':
                term[f"{p}{i}"] = 1.0
        if len(term) == 0:
            continue
        hamiltonian = PauliOperator(term, False)
        trotter_circuit = simulate_hamiltonian(q, hamiltonian, t, reps)
        circuit.insert(trotter_circuit)

    prog = QProg()
    prog.insert(circuit)
    destroy_quantum_machine(machine)
    return circuit
