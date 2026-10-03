# EVAL_META: task_id=7, framework=qpanda2, class=3
import pyqpanda

machine = pyqpanda.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def create_parametrized_gate():
    theta = 0.0
    circuit = pyqpanda.QCircuit()
    circuit << pyqpanda.RX(q[0], theta)
    return circuit

machine.finalize()
