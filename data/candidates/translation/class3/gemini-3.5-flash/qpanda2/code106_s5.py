# EVAL_META: task_id=106, framework=qpanda2, class=3
import pyqpanda as pq
from qiskit import QuantumCircuit
from qiskit.quantum_info import CNOTDihedral

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def compose_cnot_dihedral():
    prog1 = pq.QProg()
    prog1 << pq.CNOT(q[0], q[1]) << pq.T(q[0])
    
    prog2 = pq.QProg()
    prog2 << pq.CNOT(q[0], q[1]) << pq.T(q[0]) << pq.X(q[1])
    
    qasm1 = pq.convert_qprog_to_qasm(prog1, machine)
    qasm2 = pq.convert_qprog_to_qasm(prog2, machine)
    
    circ1 = QuantumCircuit.from_qasm_str(qasm1)
    circ2 = QuantumCircuit.from_qasm_str(qasm2)
    
    elem1 = CNOTDihedral(circ1)
    elem2 = CNOTDihedral(circ2)
    composed_elem = elem1.compose(elem2)
    return composed_elem

machine.finalize()
