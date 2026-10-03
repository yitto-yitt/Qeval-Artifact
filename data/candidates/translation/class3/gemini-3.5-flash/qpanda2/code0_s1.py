# EVAL_META: task_id=0, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qlist = machine.qAlloc_many(24)

def create_quantum_circuit(n_qubits):
    circuit = QCircuit()
    return circuit

if __name__ == "__main__":
    machine.finalize()
