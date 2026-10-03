# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import init_quantum_machine, QMachineType, create_empty_qprog, H, S

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qvm = init_quantum_machine(QMachineType.CPU)
    qubits = qvm.qAlloc_many(2)
    prog = create_empty_qprog()
    prog << H(qubits[0]) << S(qubits[1]).control(qubits[0]) << H(qubits[1]) << S(qubits[0]).control(qubits[1]).dagger()
    return prog
