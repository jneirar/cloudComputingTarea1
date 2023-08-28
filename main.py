import virtualbox
from time import sleep
import subprocess
import re

def get_session():
    vbox = virtualbox.VirtualBox()
    session = virtualbox.Session()
    return vbox, session

def start_vm(vm_name):
    vbox, session = get_session()
    vm = vbox.find_machine(vm_name)
    if vm.state == virtualbox.library.MachineState.powered_off:
        progress = vm.launch_vm_process(session, "gui", [])
        progress.wait_for_completion()
        sleep(10)

def shutdown_vm(vm_name):
    vbox, _ = get_session()
    vm = vbox.find_machine(vm_name)
    if vm.state == virtualbox.library.MachineState.running:
        session = vm.create_session()
        session.console.power_down()

def resume_vm(vm_name):
    vbox, _ = get_session()
    vm = vbox.find_machine(vm_name)
    if vm.state == virtualbox.library.MachineState.paused:
        session = vm.create_session()
        session.console.resume()

def suspend_vm(vm_name):
    vbox, _ = get_session()
    vm = vbox.find_machine(vm_name)
    if vm.state == virtualbox.library.MachineState.running:
        session = vm.create_session()
        session.console.pause()

def get_vm_metrics(vm_name):
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe"
    result = subprocess.check_output([vboxmanage_path, "metrics", "query", vm_name, "CPU/Load/User,RAM/Usage/Used"], text=True)
    cpu_match = re.search(r"CPU/Load/User\s+(\d+.\d+)%", result)
    ram_match = re.search(r"RAM/Usage/Used\s+(\d+) kB", result)
    cpu_usage = cpu_match.group(1) if cpu_match else "N/A"
    ram_usage = ram_match.group(1) if ram_match else "N/A"
    return cpu_usage, ram_usage

def monitor_vm(vm_name):
    for _ in range(9):
        cpu_usage, ram_usage = get_vm_metrics(vm_name)
        print(f"CPU Load: {cpu_usage} % \t\t RAM Usage: {ram_usage} KB")
        sleep(5)

def main():
    vm_name = input("Nombre de la VM: ")

    while True:
        print("\nEscoge una opción:")
        print("1. Start")
        print("2. Shutdown")
        print("3. Resume")
        print("4. Suspend")
        print("5. Monitoreo")
        print("6. Salir")
        op = input("Ingresa una opción: ")

        if op == "1":
            start_vm(vm_name)
        elif op == "2":
            shutdown_vm(vm_name)
        elif op == "3":
            resume_vm(vm_name)
        elif op == "4":
            suspend_vm(vm_name)
        elif op == "5":
            monitor_vm(vm_name)
        elif op == "6":
            break
        else:
            print("Inválido")

if __name__ == "__main__":
    main()
