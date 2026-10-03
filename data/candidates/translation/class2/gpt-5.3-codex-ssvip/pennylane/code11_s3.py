# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    num_wires = circuit.num_qubits
    dev = qml.device("default.qubit", wires=num_wires)

    @qml.qnode(dev)
    def _state():
        for instr, qargs, cargs in circuit.data:
            name = instr.name
            params = [float(p) for p in instr.params]
            wires = [q._index for q in qargs]

            if name == "id":
                qml.Identity(wires=wires[0])
            elif name == "x":
                qml.PauliX(wires=wires[0])
            elif name == "y":
                qml.PauliY(wires=wires[0])
            elif name == "z":
                qml.PauliZ(wires=wires[0])
            elif name == "h":
                qml.Hadamard(wires=wires[0])
            elif name == "s":
                qml.S(wires=wires[0])
            elif name == "sdg":
                qml.adjoint(qml.S)(wires=wires[0])
            elif name == "t":
                qml.T(wires=wires[0])
            elif name == "tdg":
                qml.adjoint(qml.T)(wires=wires[0])
            elif name == "sx":
                qml.SX(wires=wires[0])
            elif name == "sxdg":
                qml.adjoint(qml.SX)(wires=wires[0])
            elif name == "rx":
                qml.RX(params[0], wires=wires[0])
            elif name == "ry":
                qml.RY(params[0], wires=wires[0])
            elif name == "rz":
                qml.RZ(params[0], wires=wires[0])
            elif name == "p":
                qml.PhaseShift(params[0], wires=wires[0])
            elif name == "u":
                qml.U3(params[0], params[1], params[2], wires=wires[0])
            elif name == "u1":
                qml.PhaseShift(params[0], wires=wires[0])
            elif name == "u2":
                qml.U3(params[0], params[1], params[2], wires=wires[0])
            elif name == "u3":
                qml.U3(params[0], params[1], params[2], wires=wires[0])
            elif name == "cx":
                qml.CNOT(wires=wires)
            elif name == "cy":
                qml.CY(wires=wires)
            elif name == "cz":
                qml.CZ(wires=wires)
            elif name == "swap":
                qml.SWAP(wires=wires)
            elif name == "cp":
                qml.ControlledPhaseShift(params[0], wires=wires)
            elif name == "crx":
                qml.CRX(params[0], wires=wires)
            elif name == "cry":
                qml.CRY(params[0], wires=wires)
            elif name == "crz":
                qml.CRZ(params[0], wires=wires)
            elif name == "ch":
                qml.CH(wires=wires)
            elif name == "csx":
                qml.CSX(wires=wires)
            elif name == "ccx":
                qml.Toffoli(wires=wires)
            elif name == "cswap":
                qml.CSWAP(wires=wires)
            elif name == "rxx":
                qml.IsingXX(params[0], wires=wires)
            elif name == "ryy":
                qml.IsingYY(params[0], wires=wires)
            elif name == "rzz":
                qml.IsingZZ(params[0], wires=wires)
            elif name == "rzx":
                qml.QubitUnitary(qml.RZX(params[0], wires=[0, 1]).matrix(), wires=wires)
            elif name == "ecr":
                qml.QubitUnitary(instr.to_matrix(), wires=wires)
            elif name in ("barrier", "measure"):
                pass
            else:
                qml.QubitUnitary(instr.to_matrix(), wires=wires)

        return qml.state()

    return _state()
