from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    circuit = QuantumCircuit(len(state))
    for index, basis_value in enumerate(basis):
        if state[index] == 1:
            circuit.x(index)
        if basis_value == 1:
            circuit.h(index)
    return circuit
