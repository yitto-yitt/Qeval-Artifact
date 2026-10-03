# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import *

def rx_gate(value=None):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc()
    
    if value is not None:
        circuit = QCircuit()
        circuit.insert(RX(q, value))
        circuit.machine = machine
        return circuit
    else:
        vqc = VariationalQuantumCircuit()
        theta = var(0.0, True)
        vqc.insert(VariationalQuantumGate_RX(q, theta))
        vqc.machine = machine
        return vqc
