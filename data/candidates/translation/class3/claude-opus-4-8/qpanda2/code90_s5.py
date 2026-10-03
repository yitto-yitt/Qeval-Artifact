# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)


def create_custom_controlled():
    prog = QProg()

    x_gate = X(qubits[1]).control([qubits[0], qubits[3]])
    h_gate = H(qubits[2]).control([qubits[0], qubits[3]])

    prog << x_gate << h_gate

    return prog


if __name__ == "__main__":
    circuit = create_custom_controlled()
    print(circuit)
    machine.finalize()
