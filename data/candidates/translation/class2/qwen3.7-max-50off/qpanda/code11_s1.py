# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core.simulator import StateVectorSimulator

def get_statevector(circuit):
    sim = StateVectorSimulator()
    n = getattr(circuit, 'qubit_num', getattr(circuit, 'num_qubits', len(circuit.qubits)))
    sim.init(n)
    sim.run(circuit)
    return sim.get_state_vector()
