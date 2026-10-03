# EVAL_META: task_id=7, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_parametrized_gate():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc()
    theta = pq.Var(0.0)
    quantum_circuit = pq.QCircuit()
    quantum_circuit << pq.RX(q, theta)
    return quantum_circuit
