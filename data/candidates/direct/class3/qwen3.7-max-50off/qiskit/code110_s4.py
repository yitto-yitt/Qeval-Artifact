from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford
import numpy as np


def equivalent_clifford_circuit(circuit, n):
    cliff = Clifford(circuit)
    num_qubits = circuit.num_qubits
    results = []

    for i in range(n):
        equiv_circuit = cliff.to_circuit()

        num_insertions = np.random.randint(3, 10)
        for _ in range(num_insertions):
            op_type = np.random.randint(0, 6)

            if op_type == 0:
                qubit = np.random.randint(0, num_qubits)
                equiv_circuit.h(qubit)
                equiv_circuit.h(qubit)
            elif op_type == 1:
                qubit = np.random.randint(0, num_qubits)
                equiv_circuit.s(qubit)
                equiv_circuit.sdg(qubit)
            elif op_type == 2:
                qubit = np.random.randint(0, num_qubits)
                equiv_circuit.x(qubit)
                equiv_circuit.x(qubit)
            elif op_type == 3:
                qubit = np.random.randint(0, num_qubits)
                equiv_circuit.y(qubit)
                equiv_circuit.y(qubit)
            elif op_type == 4:
                qubit = np.random.randint(0, num_qubits)
                equiv_circuit.z(qubit)
                equiv_circuit.z(qubit)
            elif op_type == 5:
                if num_qubits >= 2:
                    q1 = np.random.randint(0, num_qubits)
                    q2 = np.random.randint(0, num_qubits - 1)
                    if q2 >= q1:
                        q2 += 1
                    equiv_circuit.cx(q1, q2)
                    equiv_circuit.cx(q1, q2)

        results.append(equiv_circuit)

    return results
