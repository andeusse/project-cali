import moment from 'moment';

export default class Constants {
  public static QUERY_TIME_OFFLINE: number = 2000;
  public static QUERY_TIME_ONLINE: number = 3000;

  public static QUERY_TIME_OFFLINE_TOWER: number = 10000;
  public static QUERY_TIME_ONLINE_TOWER: number = 10000;

  public static QUERY_TIME_DIGITAL_TWIN_OFF_OFFLINE_BIOGAS: number = 3000;
  public static QUERY_TIME_DIGITAL_TWIN_ON_OFFLINE_BIOGAS: number = 480000;
  public static QUERY_TIME_DIGITAL_TWIN_OFF_ONLINE_BIOGAS: number = 480000;
  public static QUERY_TIME_DIGITAL_TWIN_ON_ONLINE_BIOGAS: number = 480000;

  public static MAX_RETRIES_BEFORE_STOP: number = 5;

  public static INACTIVITY_TIMEOUT: number = 5000;

  public static NO_API_CONNECTION: string =
    'Error de conexión. Revise su conexión. Si el error persiste comuníquese con el administrador de la red';
  public static WRONG_PASSWORD: string = 'Contraseña incorrecta';

  public static LAMPS_HEIGHT_VALUES: number[] = [36, 50, 63, 83, 93];

  public static GetErrorWithDate = (
    message: string,
    code: string | undefined
  ) => {
    if (code === undefined)
      return `${moment()}: Error al realizar la consulta con mensaje de error: ${message}`;
    return `${moment()}: Error al realizar la consulta con mensaje de error: ${message} y con el código: ${code}`;
  };

  public static GetWrongFormatError = (type: string) => {
    return `El archivo no corresponde a un gemelo digital tipo ${type}`;
  };
}
