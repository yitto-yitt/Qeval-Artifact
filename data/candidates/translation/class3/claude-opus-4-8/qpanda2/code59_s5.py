# EVAL_META: task_id=59, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_cz_gate():
    circuit = QCircuit()
    circuit << H(qubits[1])
    circuit << CNOT(qubits[0], qubits[1])
    circuit << H(qubits[1])
    return circuit

if __name__ == "__main__":
    cz = create_cz_gate()
    prog = QProg()
    prog << cz
    print(prog)
    machine.finalize()
