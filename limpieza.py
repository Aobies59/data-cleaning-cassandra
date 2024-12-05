from dataclasses import dataclass, asdict
from datetime import datetime
import re
import json
import os

@dataclass
class Fecha:
    Dia: int
    Mes: int
    Año: int

    def toStr(self):
        diaStr = str(self.Dia) if self.Dia >= 10 else "0" + str(self.Dia)
        mesStr = str(self.Mes) if self.Mes >= 10 else "0" + str(self.Mes)
        añoStr = str(self.Año)
        if len(añoStr) == 2:
            if self.Año <= 24:
                añoStr = f"20{añoStr}"
            else:
                añoStr = f"19{añoStr}"
        return f"{diaStr}/{mesStr}/{añoStr}"

@dataclass
class Hora:
    Hora: int
    Minuto: int
    Segundo: int

    def toStr(self):
        horaStr = str(self.Hora) if self.Hora >= 10 else "0" + str(self.Hora)
        minutoStr = str(self.Minuto) if self.Minuto >= 10 else "0" + str(self.Minuto)
        segundoStr = str(self.Segundo) if self.Segundo >= 10 else "0" + str(self.Segundo)
        return f"{horaStr}:{minutoStr}:{segundoStr}"

@dataclass
class Carretera:
    Nombre: str
    LimiteVelocidad: int

@dataclass
class Registro:
    ID: str
    Archivo: str
    Fecha: str
    Hora: str
    Velocidad: int

@dataclass
class Conductor:
    DNI: str
    Nombre: str
    Apellido1: str
    Apellido2: str
    Direccion: str
    Poblado: str
    Correo: str
    Telefono: str
    FechaNacimiento: str
    TipoCarnet: str
    FechaCarnet: str

@dataclass
class Propietario:
    DNI: str
    Nombre: str
    Apellido1: str
    Apellido2: str
    Direccion: str
    Poblado: str
    Correo: str
    Telefono: str
    FechaNacimiento: str

@dataclass
class Vehiculo:
    Matricula: str
    Marca: str
    Modelo: str
    Potencia: str
    Color: str
    NumChasis: str
    FechaMatriculacion: str
    FechaITV: str
    Propietario: str

@dataclass
class Expediente:
    ID: str
    Fecha: str
    Tramo: str
    Sentido: str
    Carretera: str
    Registro: str
    Conductor: str
    Vehiculo: str

def main():
    for filename in os.listdir("data"):
        filePath = os.path.join("data", filename)
        if os.path.isfile(filePath):
            os.remove(filePath)

    with open("sample.json", encoding="latin1") as file:
        fileContent = file.read()
    data = fileContent.split("\n{")

    idsCarreteras = set()
    idsRegistros = set()
    idsConductores = set()
    idsPropietarios = set()
    idsVehiculos = set()
    idsExpedientes = set()

    firstTime = True
    for currObject in data:
        if firstTime:
            firstTime = False
        else:
            currObject = "{" + currObject
        currObject = json.loads(currObject.strip())

        # carreteras
        currCarretera = Carretera(
            Nombre=currObject["road"]["name"],
            LimiteVelocidad=currObject["road"]["speed limit"]
        )

        if currCarretera.Nombre not in idsCarreteras:
            idsCarreteras.add(currCarretera.Nombre)
            with open("data/carreteras.json", "a") as carreterasFile:
                carreterasFile.write(json.dumps(asdict(currCarretera)))
                carreterasFile.write("\n")

        # registros
        currFechaRegistro = currObject["Record"]["date"]
        currFechaRegistroItems = currFechaRegistro.split("/")
        currFechaRegistro = Fecha(
            Dia=int(currFechaRegistroItems[0]),
            Mes=int(currFechaRegistroItems[1]),
            Año=int(currFechaRegistroItems[2])
        )
        currHoraRegistro = currObject["Record"]["time"]
        currHoraRegistroItems = currHoraRegistro.split(":")
        currHoraRegistro = Hora(
            Hora=int(currHoraRegistroItems[0]),
            Minuto=int(currHoraRegistroItems[0]),
            Segundo=int(currHoraRegistroItems[0])
        )
        currRegistro = Registro(
            ID = currObject["Record"]["rec_ID"],
            Fecha = currFechaRegistro.toStr(),
            Hora = currHoraRegistro.toStr(),
            Archivo = currObject["Record"]["file"],
            Velocidad = int(currObject["Record"]["speed"])
        )
        if currRegistro.ID not in idsRegistros:
            idsRegistros.add(currRegistro.ID)
            with open("data/registros.json", "a") as registrosFile:
                registrosFile.write(json.dumps(asdict(currRegistro)))
                registrosFile.write("\n")

        #conductores
        currFechaNacimientoConductor = currObject["vehicle"]["Driver"]["Birthdate"]
        currFechaNacimientoConductorItems = currFechaNacimientoConductor.split("/")
        currConductorDict = currObject["vehicle"]["Driver"]
        currFechaNacimientoConductor = Fecha(
            Dia=int(currFechaNacimientoConductorItems[0]),
            Mes=int(currFechaNacimientoConductorItems[0]),
            Año=int(currFechaNacimientoConductorItems[0])
        )

        currFechaCarnet = currConductorDict["driving license"]["date"]
        currFechaCarnet = currFechaCarnet.split("/")
        currFechaCarnet = Fecha(
            Dia=int(currFechaNacimientoConductorItems[0]),
            Mes=int(currFechaNacimientoConductorItems[0]),
            Año=int(currFechaNacimientoConductorItems[0])
        )

        currConductor = Conductor(
            DNI = currConductorDict.get("DNI"),
            Nombre = currConductorDict.get("Name"),
            Apellido1 = currConductorDict.get("Surname"),
            Apellido2 = currConductorDict.get("Sec_Surname"),
            Direccion = currConductorDict.get("Address"),
            Poblado = currConductorDict.get("Town"),
            Correo = currConductorDict.get("Email"),
            Telefono = currConductorDict.get("Phone number"),
            FechaNacimiento = currFechaNacimientoConductor.toStr(),
            TipoCarnet = currConductorDict["driving license"].get("type"),
            FechaCarnet = currFechaCarnet.toStr()
        )

        if currConductor.DNI not in idsConductores:
            idsConductores.add(currConductor.DNI)
            with open("data/conductores.json", "a") as conductoresFile:
                conductoresFile.write(json.dumps(asdict(currConductor)))
                conductoresFile.write("\n")

        # propietarios
        currPropietarioDict = currObject["vehicle"]["Owner"]
        currFechaNacimientoPropietario = currPropietarioDict["Birthdate"]
        currFechaNacimientoPropietarioItems = currFechaNacimientoPropietario.split("/")
        currFechaNacimientoPropietario = Fecha(
            Dia = int(currFechaNacimientoPropietarioItems[0]),
            Mes = int(currFechaNacimientoPropietarioItems[1]),
            Año = int(currFechaNacimientoPropietarioItems[2])
        )

        currPropietario = Propietario(
            DNI = currPropietarioDict["DNI"],
            Nombre = currPropietarioDict["Name"],
            Apellido1 = currPropietarioDict["Surname"],
            Apellido2 = currPropietarioDict["Sec_Surname"],
            Direccion = currPropietarioDict["Address"],
            Poblado = currPropietarioDict["Town"],
            Correo = currPropietarioDict.get("Email"),
            Telefono = currPropietarioDict.get("Phone number"),
            FechaNacimiento = currFechaNacimientoPropietario.toStr()
        )
        if currPropietario.DNI not in idsPropietarios:
            idsPropietarios.add(currPropietario.DNI)
            with open("data/propietarios.json", "a") as propietariosFile:
                propietariosFile.write(json.dumps(asdict(currPropietario)))
                propietariosFile.write("\n")

        # vehiculos
        currVehiculoDict = currObject["vehicle"]

        currFechaMatriculacion = currVehiculoDict["registry date"]
        currFechaMatriculacion = re.sub(r'(\d+)(ST|ND|RD|TH)', r'\1', currFechaMatriculacion)
        currFechaMatriculacion = datetime.strptime(currFechaMatriculacion, "%A %d of %B, %Y")
        currFechaMatriculacion = Fecha(
            Dia = currFechaMatriculacion.day,
            Mes = currFechaMatriculacion.month,
            Año = currFechaMatriculacion.year
        )

        currITV = currVehiculoDict["roadworthiness"]
        currFechaITV = ""
        if isinstance(currITV, str):
            currFechaITV = currITV
        else:
            currITV = dict(currITV[-1])
            currFechaITV = currITV["MOT date"]

        currFechaITVItems = currFechaITV.split("/")
        currFechaITV = Fecha (
            Dia = int(currFechaITVItems[0]),
            Mes = int(currFechaITVItems[1]),
            Año = int(currFechaITVItems[2])
        )

        currVehiculo = Vehiculo(
            Matricula = currVehiculoDict["number plate"],
            Marca = currVehiculoDict["make"],
            Modelo = currVehiculoDict["model"],
            Potencia = currVehiculoDict["power"],
            Color = currVehiculoDict["colour"],
            NumChasis = currVehiculoDict["chassis number"],
            FechaMatriculacion = currFechaMatriculacion.toStr(),
            FechaITV = currFechaITV.toStr(),
            Propietario = currPropietario.DNI
        )

        if currVehiculo.Matricula not in idsVehiculos:
            idsVehiculos.add(currVehiculo.Matricula)
            with open("data/vehiculos.json", "a") as vehiculosFile:
                vehiculosFile.write(json.dumps(asdict(currVehiculo)))
                vehiculosFile.write("\n")

        #expedientes
        currFechaExpedienteItems = currObject["dump date"].split("/")
        currFechaExpediente = Fecha(
            Dia = int(currFechaExpedienteItems[0]),
            Mes  =int(currFechaExpedienteItems[1]),
            Año = int(currFechaExpedienteItems[2])
        )

        currExpediente = Expediente(
            ID = currObject["_id"],
            Fecha = currFechaExpediente.toStr(),
            Carretera = currCarretera.Nombre,
            Registro = currRegistro.ID,
            Conductor = currConductor.DNI,
            Vehiculo = currVehiculo.Matricula,
            Tramo = currObject["radar"]["mileage"],
            Sentido = "Ascendente" if currObject["radar"]["direction"] == "ascending" else "Descendiente"
        )
        if currExpediente.ID not in idsExpedientes:
            idsExpedientes.add(currExpediente.ID)
            with open("data/expedientes.json", "a") as expedientesFile:
                expedientesFile.write(json.dumps(asdict(currExpediente)))
                expedientesFile.write("\n")

    print("Data transformed correctly")

if __name__ == "__main__":
    main()