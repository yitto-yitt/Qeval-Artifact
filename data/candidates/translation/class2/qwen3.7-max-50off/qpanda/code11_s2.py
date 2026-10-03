# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import StateVectorSimulator

def get_statevector(circuit):
    sim = StateVectorSimulator()
    sim.init_qubit(circuit.qubits_num)
    sim.run(circuit)
    return sim.get_statevector()
