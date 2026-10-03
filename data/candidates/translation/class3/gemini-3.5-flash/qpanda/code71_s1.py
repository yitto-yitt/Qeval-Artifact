# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, H, SX, QCircuit

def create_quantum_circuit_based_h0_csx01_h1():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << SX(q[1]).control([q[0]])
    circuit << H(q[1])
    
    return circuit
