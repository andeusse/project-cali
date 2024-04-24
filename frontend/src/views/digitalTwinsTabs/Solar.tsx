import {
  Alert,
  Box,
  Grid,
  FormControl,
  TextField,
  InputLabel,
  MenuItem,
  Select,
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Typography,
} from '@mui/material';
import { useEffect, useState } from 'react';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import {
  SOLAR_WIND,
  SOLAR_WIND_DIAGRAM_VARIABLES,
  SolarWindParameters,
  OperationModeType,
  OperationModeText,
  SolarWindOutput,
} from '../../types/models/solar';
import { setFormState } from '../../utils/setFormState';
import Iframe from 'react-iframe';
import Config from '../../config/config';
import TimeGraphs from '../../components/models/common/TimeGraphs';
import PlayerControls from '../../components/UI/PlayerControls';
import { useControlPlayer } from '../../hooks/useControlPlayer';
import Diagram from '../../components/UI/Diagram';
import solarDiagram from '../../assets/solarDiagram.svg';
import ToggleCustomNumberField from '../../components/UI/ToggleCustomNumberField';
import CustomNumberField from '../../components/UI/CustomNumberField';
import { getValueByKey } from '../../utils/getValueByKey';
import SolarPanel from '../../components/models/SolarPanel';
import Battery from '../../components/models/Battery';
import CustomToggle from '../../components/UI/CustomToggle';

import solarIllustration from '../../assets/illustrations/solar.jpg';

type Props = {};

const Solar = (props: Props) => {
  const [solarWind, setSolarWind] = useState<SolarWindParameters>(SOLAR_WIND);
  const [isImageExpanded, setIsImageExpanded] = useState(true);
  const [isParametersExpanded, setIsParametersExpanded] = useState(true);

  const [data, graphs, isPlaying, error, onPlay, onPause, onStop] =
    useControlPlayer<SolarWindParameters, SolarWindOutput>('solar', solarWind);

  useEffect(() => {
    setIsImageExpanded(!isPlaying);
    setIsParametersExpanded(!isPlaying);
  }, [isPlaying]);

  const handleChange = (e: any, variableName?: string) => {
    const newState = setFormState<SolarWindParameters>(
      e,
      solarWind,
      variableName
    );
    if (newState) {
      setSolarWind(newState as SolarWindParameters);
    }
  };

  const playerControl = (
    <PlayerControls
      isPlaying={isPlaying}
      onPlay={onPlay}
      onPause={onPause}
      onStop={onStop}
    ></PlayerControls>
  );

  const handleImageExpanded = () => {
    setIsImageExpanded(!isImageExpanded);
  };

  const handleParametersExpanded = () => {
    setIsParametersExpanded(!isParametersExpanded);
  };

  return (
    <>
      {error !== '' && isPlaying && (
        <Alert severity="error" variant="filled">
          {error}
        </Alert>
      )}
      <Grid container spacing={2}>
        <Grid item xs={12} md={12} xl={12}>
          <Accordion expanded={isImageExpanded} onChange={handleImageExpanded}>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1-content"
              id="panel1-header"
              sx={{ margin: 0 }}
            >
              <Typography variant="h4">Sistema</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <img
                style={{
                  height: '300px',
                  display: 'block',
                  marginLeft: 'auto',
                  marginRight: 'auto',
                }}
                src={solarIllustration}
                alt="solarIllustration"
              ></img>
            </AccordionDetails>
          </Accordion>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <Accordion
            expanded={isParametersExpanded}
            onChange={handleParametersExpanded}
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel2-content"
              id="panel2-header"
              sx={{ margin: 0 }}
            >
              <Typography variant="h4">Parámetros del sistema</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6} xl={4}>
                  <FormControl fullWidth>
                    <InputLabel>Modo de operación</InputLabel>
                    <Select
                      label="Modo de operación"
                      value={solarWind.inputOperationMode}
                      name="inputOperationMode"
                      onChange={(e: any) => handleChange(e)}
                    >
                      {Object.keys(OperationModeType).map((key) => (
                        <MenuItem key={key} value={key}>
                          {getValueByKey(OperationModeText, key)}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6} xl={8}>
                  <FormControl fullWidth>
                    <TextField
                      label="Nombre"
                      value={solarWind.name}
                      name="name"
                      autoComplete="off"
                      onChange={handleChange}
                    />
                  </FormControl>
                </Grid>
                {solarWind.inputOperationMode !== OperationModeType.Mode4 && (
                  <>
                    <Grid item xs={12} md={6} xl={3}>
                      <SolarPanel
                        name="monocristalino"
                        propertyName="monocrystallinePanel"
                        handleChange={handleChange}
                        panel={solarWind.monocrystallinePanel}
                      ></SolarPanel>
                    </Grid>
                    <Grid item xs={12} md={6} xl={3}>
                      <SolarPanel
                        name="policristalino"
                        propertyName="policrystallinePanel"
                        handleChange={handleChange}
                        panel={solarWind.policrystallinePanel}
                      ></SolarPanel>
                    </Grid>
                    <Grid item xs={12} md={6} xl={3}>
                      <SolarPanel
                        name="monocristalino flexible"
                        propertyName="flexPanel"
                        handleChange={handleChange}
                        panel={solarWind.flexPanel}
                      ></SolarPanel>
                    </Grid>
                  </>
                )}
                {solarWind.inputOperationMode === OperationModeType.Mode1 && (
                  <Grid item xs={12} md={6} xl={3}>
                    <SolarPanel
                      name="telururo de cadmio"
                      propertyName="cadmiumTelluridePanel"
                      handleChange={handleChange}
                      panel={solarWind.cadmiumTelluridePanel}
                    ></SolarPanel>
                  </Grid>
                )}
                {(solarWind.inputOperationMode === OperationModeType.Mode4 ||
                  solarWind.inputOperationMode === OperationModeType.Mode5) && (
                  <Grid item xs={12} md={6} xl={3}>
                    <h3>Aerogenerador</h3>
                    <Grid container spacing={2}>
                      <Grid item xs={6} md={12} xl={12}>
                        <CustomNumberField
                          variable={solarWind.windTurbine.peakPower}
                          name="windTurbine.peakPower"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={12} xl={6}>
                        <CustomNumberField
                          variable={solarWind.windTurbine.rotorHeight}
                          name="windTurbine.rotorHeight"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={12} xl={6}>
                        <CustomNumberField
                          variable={solarWind.windTurbine.anemometerHeight}
                          name="windTurbine.anemometerHeight"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={12}>
                        <CustomNumberField
                          variable={solarWind.windTurbine.ratedWindSpeed}
                          name="windTurbine.ratedWindSpeed"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={12}>
                        <CustomNumberField
                          variable={solarWind.windTurbine.lowerCutoffWindSpeed}
                          name="windTurbine.lowerCutoffWindSpeed"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={12}>
                        <CustomNumberField
                          variable={solarWind.windTurbine.upperCutoffWindSpeed}
                          name="windTurbine.upperCutoffWindSpeed"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                    </Grid>
                  </Grid>
                )}
                {!solarWind.hybridInverter.isConnected && (
                  <Grid item xs={12} md={6} xl={3}>
                    <h3>Controlador carga</h3>
                    <Grid container spacing={2}>
                      <Grid
                        item
                        xs={12}
                        md={12}
                        xl={12}
                        alignContent={'center'}
                        height={'72px'}
                      >
                        <CustomToggle
                          name="controller.customize"
                          value={solarWind.controller.customize}
                          handleChange={handleChange}
                        ></CustomToggle>
                      </Grid>
                      <Grid item xs={6} md={6} xl={6}>
                        <CustomNumberField
                          variable={solarWind.controller.efficiency}
                          name="controller.efficiency"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={6}>
                        <CustomNumberField
                          variable={solarWind.controller.chargeVoltageBulk}
                          name="controller.chargeVoltageBulk"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={6}>
                        <CustomNumberField
                          variable={solarWind.controller.chargeVoltageFloat}
                          name="controller.chargeVoltageFloat"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                      <Grid item xs={6} md={6} xl={6}>
                        <CustomNumberField
                          variable={solarWind.controller.chargingMinimunVoltage}
                          name="controller.chargingMinimunVoltage"
                          handleChange={handleChange}
                        ></CustomNumberField>
                      </Grid>
                    </Grid>
                  </Grid>
                )}
                {((solarWind.inputOperationMode === OperationModeType.Mode1 &&
                  solarWind.cadmiumTelluridePanel.isConnected) ||
                  solarWind.inputOperationMode === OperationModeType.Mode2) && (
                  <Grid item xs={12} md={6} xl={3}>
                    <Grid container spacing={2}>
                      {((solarWind.inputOperationMode ===
                        OperationModeType.Mode1 &&
                        solarWind.cadmiumTelluridePanel.isConnected) ||
                        solarWind.inputOperationMode ===
                          OperationModeType.Mode2) && (
                        <>
                          <Grid item xs={12} md={6} xl={6}>
                            <h3>Inversor offgrid</h3>
                          </Grid>
                          <Grid
                            item
                            xs={12}
                            md={12}
                            xl={12}
                            alignContent={'center'}
                          >
                            <CustomToggle
                              name="offgridInverter.isConnected"
                              value={solarWind.offgridInverter.isConnected}
                              handleChange={handleChange}
                              trueString="Conectado"
                              falseString="Desconectado"
                              disabled={
                                solarWind.offgridInverter.isConnectedDisabled
                              }
                            ></CustomToggle>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={solarWind.offgridInverter.efficiency}
                              name="offgridInverter.efficiency"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={solarWind.offgridInverter.nominalPower}
                              name="offgridInverter.nominalPower"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                        </>
                      )}
                      {solarWind.inputOperationMode ===
                        OperationModeType.Mode2 && (
                        <>
                          <Grid
                            item
                            xs={12}
                            md={6}
                            xl={6}
                            sx={{ height: '72px' }}
                          >
                            <h3>Inversor híbrido</h3>
                          </Grid>
                          <Grid
                            item
                            xs={12}
                            md={12}
                            xl={12}
                            alignContent={'center'}
                            height={'72px'}
                          >
                            <CustomToggle
                              name="hybridInverter.isConnected"
                              value={solarWind.hybridInverter.isConnected}
                              handleChange={handleChange}
                              trueString="Conectado"
                              falseString="Desconectado"
                              disabled={
                                solarWind.hybridInverter.isConnectedDisabled
                              }
                            ></CustomToggle>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={solarWind.hybridInverter.efficiency}
                              name="hybridInverter.efficiency"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                          <Grid item xs={6} md={6} xl={6}>
                            <CustomNumberField
                              variable={solarWind.hybridInverter.nominalPower}
                              name="hybridInverter.nominalPower"
                              handleChange={handleChange}
                            ></CustomNumberField>
                          </Grid>
                        </>
                      )}
                    </Grid>
                  </Grid>
                )}
                <Grid item xs={12} md={6} xl={3}>
                  <Grid container>
                    <Grid item xs={12} md={12} xl={12}>
                      <h3>Batería 1:</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <Battery
                        propertyName="battery1"
                        battery={solarWind.battery1}
                        handleChange={handleChange}
                      ></Battery>
                    </Grid>{' '}
                  </Grid>
                </Grid>
                <Grid item xs={12} md={6} xl={3}>
                  <Grid container>
                    <Grid item xs={12} md={6} xl={6}>
                      <h3>Batería 2:</h3>
                    </Grid>
                    <Grid item xs={12} md={6} xl={6} alignContent={'center'}>
                      <CustomToggle
                        name="isBattery2"
                        value={solarWind.isBattery2}
                        handleChange={handleChange}
                        trueString="Conectado"
                        falseString="Desconectado"
                        disabled={
                          (solarWind.inputOperationMode ===
                            OperationModeType.Mode1 &&
                            solarWind.cadmiumTelluridePanel.isConnected) ||
                          solarWind.inputOperationMode ===
                            OperationModeType.Mode2
                        }
                      ></CustomToggle>
                    </Grid>
                    {solarWind.isBattery2 && (
                      <Grid item xs={12} md={12} xl={12}>
                        <Battery
                          propertyName="battery2"
                          battery={solarWind.battery2}
                          handleChange={handleChange}
                        ></Battery>
                      </Grid>
                    )}
                  </Grid>
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>
        </Grid>
        <Grid item xs={12} md={12} xl={12}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={3} xl={3}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={12} xl={12}>
                  <h2>Operación planta</h2>
                </Grid>
                <Grid item xs={12} md={12} xl={12} alignContent={'center'}>
                  <CustomToggle
                    name="inputOfflineOperation"
                    value={solarWind.inputOfflineOperation}
                    handleChange={handleChange}
                    trueString="Offline"
                    falseString="Online"
                  ></CustomToggle>
                </Grid>
                <Grid item xs={12} md={12} xl={12}>
                  <h3>Parámetros ambientales</h3>
                </Grid>
                <>
                  {(solarWind.monocrystallinePanel.isConnected ||
                    solarWind.policrystallinePanel.isConnected ||
                    solarWind.inputOperationMode !==
                      OperationModeType.Mode4) && (
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={solarWind.solarRadiation1}
                        name="solarRadiation1"
                        handleChange={handleChange}
                        disabled={solarWind.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                  )}
                  {(solarWind.flexPanel.isConnected ||
                    solarWind.cadmiumTelluridePanel.isConnected ||
                    solarWind.inputOperationMode !==
                      OperationModeType.Mode4) && (
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={solarWind.solarRadiation2}
                        name="solarRadiation2"
                        handleChange={handleChange}
                        disabled={solarWind.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                  )}
                  {solarWind.inputOperationMode !== OperationModeType.Mode4 && (
                    <Grid item xs={7} md={7} xl={7}>
                      <CustomNumberField
                        variable={solarWind.temperature}
                        name="temperature"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  )}
                </>
                {(solarWind.inputOperationMode === OperationModeType.Mode4 ||
                  solarWind.inputOperationMode === OperationModeType.Mode5) && (
                  <>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={solarWind.windSpeed}
                        name="windSpeed"
                        handleChange={handleChange}
                        disabled={solarWind.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                    <Grid item xs={7} md={7} xl={7}>
                      <CustomNumberField
                        variable={solarWind.windDensity}
                        name="windDensity"
                        handleChange={handleChange}
                      ></CustomNumberField>
                    </Grid>
                  </>
                )}
                {((solarWind.inputOperationMode === OperationModeType.Mode1 &&
                  solarWind.cadmiumTelluridePanel.isConnected &&
                  solarWind.offgridInverter.isConnected) ||
                  (solarWind.inputOperationMode === OperationModeType.Mode2 &&
                    (solarWind.offgridInverter.isConnected ||
                      solarWind.hybridInverter.isConnected))) && (
                  <>
                    <Grid item xs={12} md={12} xl={12}>
                      <h3>Parámetros carga CA</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={solarWind.alternCurrentLoadPower}
                        name="alternCurrentLoadPower"
                        handleChange={handleChange}
                        disabled={solarWind.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={solarWind.alternCurrentLoadPowerFactor}
                        name="alternCurrentLoadPowerFactor"
                        handleChange={handleChange}
                        disabled={solarWind.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                  </>
                )}
                {!(
                  solarWind.inputOperationMode === OperationModeType.Mode2 &&
                  solarWind.hybridInverter.isConnected
                ) && (
                  <>
                    <Grid item xs={12} md={12} xl={12}>
                      <h3>Parámetros carga CD</h3>
                    </Grid>
                    <Grid item xs={12} md={12} xl={12}>
                      <ToggleCustomNumberField
                        variable={solarWind.directCurrentLoadPower}
                        name="directCurrentLoadPower"
                        handleChange={handleChange}
                        disabled={solarWind.inputOfflineOperation}
                      ></ToggleCustomNumberField>
                    </Grid>
                  </>
                )}
                {solarWind.inputOperationMode === OperationModeType.Mode2 &&
                  solarWind.hybridInverter.isConnected && (
                    <>
                      <Grid item xs={12} md={12} xl={12}>
                        <h3>Parámetros red externa</h3>
                      </Grid>
                      <Grid
                        item
                        xs={12}
                        md={12}
                        xl={12}
                        alignContent={'center'}
                      >
                        <CustomToggle
                          name="externalGridState"
                          value={solarWind.externalGridState}
                          handleChange={handleChange}
                          trueString="Conectado"
                          falseString="Desconectado"
                        ></CustomToggle>
                      </Grid>
                    </>
                  )}
              </Grid>
            </Grid>
            <Grid item xs={12} md={9} xl={9}>
              <Iframe
                styles={{
                  width: '100%',
                  height: '250px',
                }}
                url={Config.getInstance().params.windyUrl}
              ></Iframe>
              {playerControl}
              <Diagram<{}>
                diagram={solarDiagram}
                data={data}
                variables={SOLAR_WIND_DIAGRAM_VARIABLES}
                width={800}
                height={400}
              ></Diagram>
            </Grid>
          </Grid>
        </Grid>
        {graphs !== undefined && solarWind.timeMultiplier && (
          <>
            <Grid item xs={12} md={12} xl={12}>
              <TimeGraphs
                timeMultiplier={solarWind.timeMultiplier}
                handleChange={handleChange}
                graphs={graphs}
                variables={SOLAR_WIND_DIAGRAM_VARIABLES}
                playerControl={playerControl}
                isPlaying={isPlaying}
              ></TimeGraphs>
            </Grid>
          </>
        )}
      </Grid>
    </>
  );
};

export default Solar;
