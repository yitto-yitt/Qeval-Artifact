# EVAL_META: task_id=71, framework=qpanda2, class=3
from pyqpanda import CPUQVM, H, X, U1

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    prog = []
    prog.append(H(qubits[0]))
    # Controlled-SX on control=0, target=1
    # SX = sqrt(X); implement CSX via H on target, then controlled-S (phase), then H
    prog.append(H(qubits[1]))
    prog.append(U1(qubits[1], 3.141592653589793 / 2).control([qubits[0]]))
    prog.append(H(qubits[1]))
    prog.append(H(qubits[1]))
    return prog

if __name__ == "__main__":
    circuit = create_quantum_circuit_based_h0_csx01_h1()
    from pyqpanda import QProg
    prog = QProg()
    for gate in circuit:
        prog << gate
    print(prog)
    machine.finalize()
