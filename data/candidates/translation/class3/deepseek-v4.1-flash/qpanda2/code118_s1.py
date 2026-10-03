# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)


def create_c3sx_circuit():
    circuit = QCircuit()
    circuit << H(qubits[3])
    s_gate = S(qubits[3])
    s_gate = s_gate.control([qubits[0], qubits[1], qubits[2]])
    circuit << s_gate
    circuit << H(qubits[3])
    return circuit


if __name__ == "__main__":
    machine.finalize()
