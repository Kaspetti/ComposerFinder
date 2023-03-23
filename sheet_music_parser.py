import numpy as np
import xml.etree.ElementTree as ET

duration_types = {
    "32nd": "01",
    "16th": "02",
    "eighth": "04",
    "quarter": "08",
    "half": "16",
    "whole": "32"   
}

'''spanner_types = {
       "Slur" : "1",
       "Tie" : "2",
       "HairPin" : "3",
       
}'''

def parseXML(file: str):
    parsed_staff_1 = []
    parsed_staff_2 = []
    
    tree = ET.parse(file)
    root = tree.getroot()
    staves = root.findall("./Score/Staff")
    
    for staff in staves:
        measures = staff.findall("./Measure")
        for measure in measures:
            parsed_measure = []
            voice = measure.find("./voice")
            chords = voice.findall("./Chord")
            
            for chord in chords:
                duration_type = chord.find("./durationType").text
                duration = duration_types[duration_type]
                dots = chord.find("./dots")
                
                notes = chord.findall("./Note")
                for note in notes:
                    pitch = note.find("./pitch").text
                    
                    # Format: <spanner>.<pitch><dots><duration>
                    note = float(
                        "0." + 
                        pitch + 
                        (dots.text if dots is not None else "0") + 
                        duration)
                    
                    parsed_measure.append(note)
        
            if staff.attrib["id"] == "1":
                parsed_staff_1.append(np.pad(parsed_measure, (0, 32 - len(parsed_measure)), 'constant', constant_values=(0, 0)))
            else:
                parsed_staff_2.append(np.pad(parsed_measure, (0, 32 - len(parsed_measure)), 'constant', constant_values=(0, 0)))
    
    return np.append(parsed_staff_1, parsed_staff_2, axis=0)

if __name__ == "__main__":
    print(parseXML("Nocturne.mscx")[1])