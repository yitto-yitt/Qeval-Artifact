# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, Sdg, CNOT, S

def create_cy_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = [qvm.qAlloc() for _ in range(2)]
    circuit = QCircuit()
    circuit << Sdg(qubits[1]) << CNOT(qubits[0], qubits[1]) << S(qubits[1])
    return circuit
