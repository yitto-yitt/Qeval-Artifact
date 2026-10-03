# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_csx01_h1():
    def _append_csx(circuit, control, target):
        if "CSX" in globals():
            try:
                circuit << globals()["CSX"](control, target)
                return
            except Exception:
                pass

        if "SX" in globals():
            try:
                gate = globals()["SX"](target)
                try:
                    controlled_gate = gate.control([control])
                except Exception:
                    controlled_gate = gate.control(control)
                if controlled_gate is not None:
                    gate = controlled_gate
                circuit << gate
                return
            except Exception:
                pass

        circuit << H(target)
        gate = S(target)
        try:
            controlled_gate = gate.control([control])
        except Exception:
            controlled_gate = gate.control(control)
        if controlled_gate is not None:
            gate = controlled_gate
        circuit << gate
        circuit << H(target)

    try:
        qc = QCircuit(3)
        qc << H(0)
        _append_csx(qc, 0, 1)
        qc << H(1)
        return qc
    except Exception:
        pass

    machine = CPUQVM()
    try:
        machine.init()
    except Exception:
        try:
            machine.init_qvm()
        except Exception:
            pass

    try:
        qubits = machine.qAlloc_many(3)
    except AttributeError:
        qubits = machine.qalloc_many(3)

    qc = QCircuit()
    qc << H(qubits[0])
    _append_csx(qc, qubits[0], qubits[1])
    qc << H(qubits[1])

    create_quantum_circuit_based_h0_csx01_h1._machine = machine
    create_quantum_circuit_based_h0_csx01_h1._qubits = qubits
    return qc
