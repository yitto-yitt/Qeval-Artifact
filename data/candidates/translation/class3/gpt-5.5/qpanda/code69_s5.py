# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    def _controlled_s(control, target):
        gate = S(target)
        try:
            controlled_gate = gate.control([control])
            return gate if controlled_gate is None else controlled_gate
        except Exception:
            gate = S(target)
            controlled_gate = gate.control(control)
            return gate if controlled_gate is None else controlled_gate

    def _controlled_sdg(control, target):
        gate = S(target)
        dagger_gate = gate.dagger()
        if dagger_gate is None:
            dagger_gate = gate
        try:
            controlled_gate = dagger_gate.control([control])
            return dagger_gate if controlled_gate is None else controlled_gate
        except Exception:
            gate = S(target)
            dagger_gate = gate.dagger()
            if dagger_gate is None:
                dagger_gate = gate
            controlled_gate = dagger_gate.control(control)
            return dagger_gate if controlled_gate is None else controlled_gate

    try:
        machine = CPUQVM()
        if hasattr(machine, "init_qvm"):
            machine.init_qvm()
        elif hasattr(machine, "init"):
            machine.init()
        q = machine.qAlloc_many(2)
        create_quantum_circuit_based_h0_cs01_h1_csdg10._machine = machine
        create_quantum_circuit_based_h0_cs01_h1_csdg10._qubits = q
    except Exception:
        q = [0, 1]

    circuit = QCircuit()
    circuit << H(q[0])
    circuit << _controlled_s(q[0], q[1])
    circuit << H(q[1])
    circuit << _controlled_sdg(q[1], q[0])
    return circuit
