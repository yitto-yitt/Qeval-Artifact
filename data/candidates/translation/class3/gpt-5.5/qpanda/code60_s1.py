# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import *

def create_cy_gate():
    def _build(q):
        circuit = QCircuit()
        sdg_gate = S(q[1])
        if hasattr(sdg_gate, "dagger"):
            sdg_gate = sdg_gate.dagger()
        else:
            sdg_gate = sdg_gate.dag()
        cnot_gate = globals().get("CNOT", globals().get("CX"))
        circuit << sdg_gate
        circuit << cnot_gate(q[0], q[1])
        circuit << S(q[1])
        return circuit

    try:
        return _build([0, 1])
    except Exception:
        machine = CPUQVM()
        try:
            machine.init_qvm()
        except Exception:
            pass
        try:
            qubits = machine.qAlloc_many(2)
        except AttributeError:
            qubits = machine.allocate_qubits(2)
        create_cy_gate._machine = machine
        create_cy_gate._qubits = qubits
        return _build(qubits)
