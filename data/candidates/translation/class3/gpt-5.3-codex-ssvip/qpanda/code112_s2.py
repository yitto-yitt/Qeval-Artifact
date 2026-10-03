# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, init_quantum_machine, QMachineType, destroy_quantum_machine
from pyqpanda3.core import PauliOperator, simulate_pauliHamiltonian


def create_product_formula_circuit(pauli_strings, times, order, reps):
    if not pauli_strings:
        return QCircuit()

    n_qubits = len(pauli_strings[0])
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(n_qubits)

    circuit = QCircuit()
    for pauli_string, t in zip(pauli_strings, times):
        pauli_map = {}
        for i, p in enumerate(pauli_string):
            if p != 'I':
                pauli_map[f"{p}{i}"] = 1.0
        hamiltonian = PauliOperator(pauli_map, 1.0)
        term_circuit = simulate_pauliHamiltonian(qubits, hamiltonian, float(t), int(reps))
        circuit.insert(term_circuit)

    prog = QProg()
    prog.insert(circuit)
    destroy_quantum_machine(machine)
    return circuit
