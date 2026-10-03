# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import StateVectorSimulator, QProg, QCircuit

def get_statevector(circuit):
    sim = StateVectorSimulator()
    if isinstance(circuit, QCircuit):
        prog = QProg()
        prog << circuit
    else:
        prog = circuit
    sim.run(prog)
    return sim.get_state()
