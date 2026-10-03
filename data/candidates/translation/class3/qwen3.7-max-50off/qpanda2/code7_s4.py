# EVAL_META: task_id=7, framework=qpanda2, class=3
import pyqpanda

machine = pyqpanda.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def create_parametrized_gate():
    theta = 0.0
    prog = pyqpanda.QProg()
    prog << pyqpanda.RX(qubits[0], theta)
    return prog

machine.finalize()
