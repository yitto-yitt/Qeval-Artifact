# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    circ = QCircuit()
    controls = [qubits[0], qubits[1], qubits[2]]
    target = qubits[3]
    circ << H(target)
    circ << S(target).control(controls)
    circ << H(target)
    return circ

if __name__ == "__main__":
    circ = create_c3sx_circuit()
    prog = QProg()
    prog << circ
    machine.run(prog)
    machine.finalize()

