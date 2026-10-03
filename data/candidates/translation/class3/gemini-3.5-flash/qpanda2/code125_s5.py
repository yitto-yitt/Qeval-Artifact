# EVAL_META: task_id=125, framework=qpanda2, class=3
import pyqpanda as pq

# Global QVM Initialization
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(16)

def circ_to_gate(circ):
    gate_circuit = pq.QCircuit()
    gate_circuit << circ
    return gate_circuit

# Manual Cleanup
machine.finalize()
