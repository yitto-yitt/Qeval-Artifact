# EVAL_META: task_id=7, framework=qpanda2, class=3
from pyqpanda import *
from pyqpanda import var

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def create_parametrized_gate():
    theta = var("theta")
    vqc = VariationalQuantumCircuit()
    vqc << RX(qubits[0], theta)
    return vqc

if __name__ == "__main__":
    machine.finalize()
