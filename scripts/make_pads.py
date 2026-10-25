import cnc_tools

p = cnc_tools.pads()
with open('pads.nc','w') as file:
    file.write(p)
