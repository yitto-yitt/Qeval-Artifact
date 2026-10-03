# EVAL_META: task_id=0, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg
def create_quantum_circuit(n_qubits):
    machine = CPUQVM()
    machine.init_qvm()
    qlist = machine.qAlloc_many(n_qubits)
    circuit = QProg()
    return circuit
