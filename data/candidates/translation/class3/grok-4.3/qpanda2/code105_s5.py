# EVAL_META: task_id=105, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
def initialize_cnot_dihedral():
    circuit = QCircuit()
    circuit << CNOT(qubits[0], qubits[1]) << T(qubits[0])
    prog = QProg()
    prog << circuit
    machine.directly_run(prog)
    return circuit
machine.finalize()
