# EVAL_META: task_id=89, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_controlled_hgate():
    prog = QProg()
    h_gate = H(qubits[2])
    h_gate.set_control([qubits[0], qubits[1]])
    prog << h_gate
    return prog

if __name__ == "__main__":
    circuit = create_controlled_hgate()
    print(circuit)
    machine.finalize()
