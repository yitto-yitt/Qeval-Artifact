# EVAL_META: task_id=69, framework=qpanda2, class=3
from pyqpanda import *

# Global QVM initialization
machine = init_quantum_machine(QMachineType.CPU)
qubits = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    prog = QProg()
    prog << H(qubits[0])
    prog << S(qubits[1]).control([qubits[0]])
    prog << H(qubits[1])
    prog << S(qubits[0]).dagger().control([qubits[1]])
    return prog

machine.finalize()
