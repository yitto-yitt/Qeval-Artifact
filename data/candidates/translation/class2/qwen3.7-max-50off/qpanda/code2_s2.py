# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit, StateVectorSimulator

def create_bell_statevector():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    sim = StateVectorSimulator()
    sim.run(qc)
    return sim.get_state()
