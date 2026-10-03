# EVAL_META: task_id=89, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, H

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def create_controlled_hgate():
    circuit = QCircuit()
    h_gate = H(qubits[2])
    controlled_h = h_gate.control([qubits[0], qubits[1]])
    circuit << controlled_h
    return circuit


if __name__ == "__main__":
    qc = create_controlled_hgate()
    prog = QCircuit()
    prog << qc
    print(qc)
    machine.finalize()
