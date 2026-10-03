# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *

def create_efficientSU2():
    machine = QuantumMachine()
    q = machine.qAlloc_many(3)
    circuit = QCircuit()
    params = [machine.alloc_and_assign_param(f"theta_{i}") for i in range(12)]
    for i in range(3):
        circuit.insert(RZ(q[i], params[2*i]))
        circuit.insert(RY(q[i], params[2*i+1]))
    circuit.insert(BARRIER(q))
    circuit.insert(CNOT(q[0], q[1]))
    circuit.insert(CNOT(q[0], q[2]))
    circuit.insert(CNOT(q[1], q[2]))
    circuit.insert(BARRIER(q))
    for i in range(3):
        circuit.insert(RZ(q[i], params[6+2*i]))
        circuit.insert(RY(q[i], params[6+2*i+1]))
    return circuit
