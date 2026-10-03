# EVAL_META: task_id=7, framework=qpanda2, class=3
from pyqpanda import CPUQVM, VariationalQuantumCircuit, VariationalQuantumGate, GateType

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def create_parametrized_gate():
    theta = 0.0
    circuit = VariationalQuantumCircuit()
    circuit.insert(VariationalQuantumGate(GateType.RX_GATE, [q[0]], [theta]))
    return circuit

machine.finalize()
