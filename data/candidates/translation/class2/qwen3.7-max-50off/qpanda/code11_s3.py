# EVAL_META: task_id=11, framework=qpanda, class=2
import pyqpanda3 as pq

def get_statevector(circuit):
    sim = pq.StateVectorSimulator()
    sim.init_qubit(circuit.qubits_num)
    sim.run(circuit)
    return sim.get_state()
