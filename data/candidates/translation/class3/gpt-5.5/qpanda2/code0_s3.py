# EVAL_META: task_id=0, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def create_quantum_circuit(n_qubits):
    return QCircuit()

machine.finalize()
