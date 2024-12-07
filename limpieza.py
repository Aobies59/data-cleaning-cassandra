from dataclasses import dataclass
from datetime import datetime
import re
import json

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
        return f"{añoStr}-{mesStr}-{diaStr}"

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
    LimiteRadar: int
    Multa: bool
    Carretera: str
    Registro: str
    Conductor: str
    Vehiculo: str

CARRETERAS_FILENAME = "data/carreteras.csv"
CONDUCTORES_FILENAME = "data/conductores.csv"
EXPEDIENTES_FILENAME = "data/expedientes.csv"
PROPIETARIOS_FILENAME = "data/propietarios.csv"
REGISTROS_FILENAME = "data/registros.csv"
VEHICULOS_FILENAME = "data/vehiculos.csv"

def main():
    with open("sample.json", encoding="latin1") as file:
        fileContent = file.read()
    data = fileContent.split("\n{")

    idsCarreteras = set()
    idsRegistros = set()
    idsConductores = set()
    idsPropietarios = set()
    idsVehiculos = set()
    idsExpedientes = set()

    with open(CARRETERAS_FILENAME, "w") as file:
        file.write("Nombre;LimiteVelocidad\n")

    with open(REGISTROS_FILENAME, "w") as file:
        file.write("ID;Archivo;Fecha;Hora;Velocidad\n")

    with open(CONDUCTORES_FILENAME, "w") as file:
        file.write("DNI;Nombre;Apellido1;Apellido2;Direccion;Poblado;Correo;Telefono;FechaNacimiento;TipoCarnet;FechaCarnet\n")

    with open(PROPIETARIOS_FILENAME, "w") as file:
        file.write("DNI;Nombre;Apellido1;Apellido2;Direccion;Poblado;Correo;Telefono;FechaNacimiento\n")

    with open(VEHICULOS_FILENAME, "w") as file:
        file.write("Matricula;Marca;Modelo;Potencia;Color;NumChasis;FechaMatriculacion;FechaITV;Propietario\n")

    with open(EXPEDIENTES_FILENAME, "w") as file:
        file.write("ID;Fecha;Tramo;Sentido;LimiteRadar;Multa;Carretera;Registro;Conductor;Vehiculo\n")

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
            with open(CARRETERAS_FILENAME, "a") as carreterasFile:
                carreterasFile.write(f"{currCarretera.Nombre};{currCarretera.LimiteVelocidad}\n")

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
            Minuto=int(currHoraRegistroItems[1]),
            Segundo=int(currHoraRegistroItems[2].split(".")[0])
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
            with open(REGISTROS_FILENAME, "a") as registrosFile:
                registrosFile.write(f"{currRegistro.ID};{currRegistro.Archivo};{currRegistro.Fecha};{currRegistro.Hora};{currRegistro.Velocidad}\n")

        #conductores
        currFechaNacimientoConductor = currObject["vehicle"]["Driver"]["Birthdate"]
        currFechaNacimientoConductorItems = currFechaNacimientoConductor.split("/")
        currConductorDict = currObject["vehicle"]["Driver"]
        currFechaNacimientoConductor = Fecha(
            Dia=int(currFechaNacimientoConductorItems[0]),
            Mes=int(currFechaNacimientoConductorItems[1]),
            Año=int(currFechaNacimientoConductorItems[2])
        )

        currFechaCarnet = currConductorDict["driving license"]["date"]
        currFechaCarnet = currFechaCarnet.split("/")
        currFechaCarnet = Fecha(
            Dia=int(currFechaNacimientoConductorItems[0]),
            Mes=int(currFechaNacimientoConductorItems[1]),
            Año=int(currFechaNacimientoConductorItems[2])
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
            with open(CONDUCTORES_FILENAME, "a") as conductoresFile:
                conductoresFile.write(f"{currConductor.DNI};{currConductor.Nombre};{currConductor.Apellido1};{currConductor.Apellido2};{currConductor.Direccion};{currConductor.Poblado};{currConductor.Correo};{currConductor.Telefono};{currConductor.FechaNacimiento};{currConductor.TipoCarnet};{currConductor.FechaCarnet}\n")

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
            with open(PROPIETARIOS_FILENAME, "a") as propietariosFile:
                propietariosFile.write(f"{currPropietario.DNI};{currPropietario.Nombre};{currPropietario.Apellido1};{currPropietario.Apellido2};{currPropietario.Direccion};{currPropietario.Poblado};{currPropietario.Correo};{currPropietario.Telefono};{currPropietario.FechaNacimiento}\n")

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
            with open(VEHICULOS_FILENAME, "a") as vehiculosFile:
                vehiculosFile.write(f"{currVehiculo.Matricula};{currVehiculo.Marca};{currVehiculo.Modelo};{currVehiculo.Potencia};{currVehiculo.Color};{currVehiculo.NumChasis};{currVehiculo.FechaMatriculacion};{currVehiculo.FechaITV};{currVehiculo.Propietario}\n")

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
            Sentido = "Ascendente" if currObject["radar"]["direction"] == "ascending" else "Descendiente",
            LimiteRadar=currObject["radar"]["speed limit"],
            Multa=True if currObject.get("Speed ticket") else False
        )
        if currExpediente.ID not in idsExpedientes:
            idsExpedientes.add(currExpediente.ID)
            with open(EXPEDIENTES_FILENAME, "a") as expedientesFile:
                expedientesFile.write(f"{currExpediente.ID};{currExpediente.Fecha};{currExpediente.Tramo};{currExpediente.Sentido};{currExpediente.LimiteRadar};{currExpediente.Multa};{currExpediente.Carretera};{currExpediente.Registro};{currExpediente.Conductor};{currExpediente.Vehiculo}\n")

    print("Data transformed correctly")

if __name__ == "__main__":
    main()
