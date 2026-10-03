# EVAL_META: task_id=23, framework=qpanda, class=3
import pyqpanda3.core as qp

def dj_constant_oracle():
    machine = qp.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    circuit = qp.QCircuit()
    circuit << qp.X(qubits[2])
    return circuit
