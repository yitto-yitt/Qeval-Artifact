# EVAL_META: task_id=105, framework=qpanda2, class=3
import atexit
import pyqpanda as pq
from qiskit import QuantumCircuit
from qiskit.quantum_info import CNOTDihedral

# Global QVM
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

# Register cleanup to be executed at the end of the script
atexit.register(machine.finalize)


def initialize_cnot_dihedral():
    prog = pq.QProg()
    prog << pq.CNOT(q[0], q[1]) << pq.T(q[0])

    qasm = pq.convert_qprog_to_qasm(prog, machine)
    circ = QuantumCircuit.from_qasm_str(qasm)
    elem = CNOTDihedral(circ)
    return elem
