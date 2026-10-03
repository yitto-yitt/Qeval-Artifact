# EVAL_META: task_id=110, framework=qpanda, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford, Operator
from pyqpanda3.core import QProg, Qubit, H, S, X, Y, Z, CNOT, CZ, SWAP

def equivalent_clifford_circuit(circuit, n):
    op_or = Operator(circuit)
    num_qubits = circuit.num_qubits
    qc_list = []
    counter = 0
    while counter < n:
        qc = random_clifford(num_qubits).to_circuit()
        op_qc = Operator(qc)
        if op_qc.equiv(op_or, rtol=0.4, atol=0.4):
            counter += 1
            qubits = [Qubit() for _ in range(num_qubits)]
            prog = QProg()
            for instr, qargs, cargs in qc.data:
                gate_name = instr.name
                q_idx = [qc.find_bit(q).index for q in qargs]
                if gate_name == 'h':
                    prog << H(qubits[q_idx[0]])
                elif gate_name == 's':
                    prog << S(qubits[q_idx[0]])
                elif gate_name == 'sdg':
                    prog << S(qubits[q_idx[0]]).dagger()
                elif gate_name == 'x':
                    prog << X(qubits[q_idx[0]])
                elif gate_name == 'y':
                    prog << Y(qubits[q_idx[0]])
                elif gate_name == 'z':
                    prog << Z(qubits[q_idx[0]])
                elif gate_name == 'cx':
                    prog << CNOT(qubits[q_idx[0]], qubits[q_idx[1]])
                elif gate_name == 'cz':
                    prog << CZ(qubits[q_idx[0]], qubits[q_idx[1]])
                elif gate_name == 'swap':
                    prog << SWAP(qubits[q_idx[0]], qubits[q_idx[1]])
            qc_list.append(prog)
    return qc_list
