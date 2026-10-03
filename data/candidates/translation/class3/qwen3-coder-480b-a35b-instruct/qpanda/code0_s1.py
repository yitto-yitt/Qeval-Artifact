# EVAL_META: task_id=0, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QMachine

def create_quantum_circuit(n_qubits):
    machine = QMachine()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n_qubits)
    circuit = QCircuit()
    machine.finalize()
    return circuit
