# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, Parameter, QuantumCircuit, RX

def create_parametrized_gate():
    qvm = CPUQVM()
    q = qvm.allocate_qubits(1)[0]
    theta = Parameter("theta")
    circuit = QuantumCircuit()
    circuit << RX(q, theta)
    return circuit
