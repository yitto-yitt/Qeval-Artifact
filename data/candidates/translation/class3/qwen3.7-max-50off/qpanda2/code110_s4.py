# EVAL_META: task_id=110, framework=qpanda2, class=3
import pyqpanda as pq
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford, Operator

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(30)

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
            prog = pq.QProg()
            for instruction, qargs, cargs in qc.data:
                gate_name = instruction.name.upper()
                qubits = [q[qc.qubits.index(qarg)] for qarg in qargs]
                
                if gate_name == 'H':
                    prog << pq.H(qubits[0])
                elif gate_name == 'S':
                    prog << pq.S(qubits[0])
                elif gate_name == 'SDG':
                    prog << pq.S(qubits[0]).dagger()
                elif gate_name == 'X':
                    prog << pq.X(qubits[0])
                elif gate_name == 'Y':
                    prog << pq.Y(qubits[0])
                elif gate_name == 'Z':
                    prog << pq.Z(qubits[0])
                elif gate_name in ['CX', 'CNOT']:
                    prog << pq.CNOT(qubits[0], qubits[1])
                elif gate_name == 'CZ':
                    prog << pq.CZ(qubits[0], qubits[1])
                elif gate_name == 'SWAP':
                    prog << pq.SWAP(qubits[0], qubits[1])
            qc_list.append(prog)
            
    return qc_list

machine.finalize()
