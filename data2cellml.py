
import sys
import csv

if len(sys.argv) < 8:
    sys.exit("invalid arguments")

filename = sys.argv[1]
timeColumn = int(sys.argv[2])
valueColumn = int(sys.argv[3])
timeUnits = sys.argv[4]
unitsName = sys.argv[5]
numberOfRepeats = int(sys.argv[6])
every = int(sys.argv[7])

offsetValues = False
if len(sys.argv) > 6:
    offsetValues = True

# Read in the data
time = []
data = []
with open(sys.argv[1], "r") as f:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        if i % every == 0:
            try:
                currentTime = float(line[timeColumn])
                currentValue = float(line[valueColumn])
                if i == 0:
                    offsetValue = currentTime
                if offsetValues:
                    currentTime = currentTime - offsetValue
                time.append(currentTime)
                data.append(currentValue)
            except ValueError:
                break

# handle repeats
finalTime = time[-1]
timeStep = time[-1] - time[-2]
timeIncrement = finalTime + timeStep

print '<?xml version="1.0"?>'
print '<model xmlns="http://www.cellml.org/cellml/1.1#" xmlns:cellml="http://www.cellml.org/cellml/1.1#" name="dataPoints">'
print '  <component name="data">'
print '    <variable name="data" units="' + unitsName + '" public_interface="out"/>'
print '    <variable name="time" units="' + timeUnits + '" public_interface="in"/>'
print '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
print '      <apply><eq/>'
print '        <ci>data</ci>'
print '        <piecewise>'

for i in range(0, numberOfRepeats):
    incT = timeIncrement * i
    for (t,d) in zip(time, data):
        currentTime = t + incT
        currentValue = d
        print '          <piece>'
        print '            <cn cellml:units="' + unitsName + '">' + str(currentValue) + '</cn>'
        print '            <apply><lt/>'
        print '                <ci>time</ci>'
        print '                <cn cellml:units="' + timeUnits + '">' + str(currentTime) + '</cn>'
        print '            </apply>'
        print '          </piece>'

print '         <otherwise>'
print '           <cn cellml:units="' + unitsName + '">' + str(currentValue) + '</cn>'
print '         </otherwise>'

print '        </piecewise>'
print '      </apply>'
print '    </math>'
print '  </component>'
print '</model>'

