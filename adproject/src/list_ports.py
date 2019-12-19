from serial.tools.list_ports import comports

for portInfo in comports():
    print(portInfo.device)
    print("   name:", portInfo.name)
    print("   description:", portInfo.description)
    print("   hwid:", portInfo.hwid)
    print("   vid:", portInfo.vid)
    print("   pid:", portInfo.pid)
    print("   serial_number:", portInfo.serial_number)
    print("   location:", portInfo.location)
    print("   manufacturer:", portInfo.manufacturer)
    print("   product:", portInfo.product)
    print("   interface:", portInfo.interface)
    print()
