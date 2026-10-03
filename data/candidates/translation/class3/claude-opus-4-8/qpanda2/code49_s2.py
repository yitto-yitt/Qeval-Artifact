# EVAL_META: task_id=49, framework=qpanda2, class=3
from pyqpanda import CPUQVM, H, CNOT, QProg

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def simple_elitzur_vaidman():
    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << H(qubits[0])
    return prog

if __name__ == "__main__":
    circuit = simple_elitzur_vaidman()
    print(circuit)
    machine.finalize()
