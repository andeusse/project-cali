import React, { useEffect, useState } from 'react';
import {
  ScenariosSolarPanelMeteorologicalInformationText,
  ScenariosSolarPanelMeteorologicalInformationType,
  SmartSystemType,
  SolarSystem,
  SolarPanelModuleText,
  SolarPanelModuleType,
  TabProps,
} from '../../../types/scenarios/common';
import {
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from '@mui/material';
import Spreadsheet, { CellBase, Matrix } from 'react-spreadsheet';
import CustomNumberField from '../../UI/CustomNumberField';
import { getValueByKey } from '../../../utils/getValueByKey';
import { useAppSelector } from '../../../redux/reduxHooks';
import { ThemeType } from '../../../types/theme';

const ROW_LABELS: string[] = ['Radiación [W / m²]', 'Temperatura [°C]'];

const SolarTab = (props: TabProps) => {
  const { system, handleSystemChange, handleTableChange } = props;

  const userTheme = useAppSelector((state) => state.theme.value);

  const [selectedElement, setSelectedElement] = useState<string | undefined>(
    system.solarSystems.length > 0 ? system.solarSystems[0].id : undefined
  );

  const [selectedSystem, setSelectedSystem] = useState<SolarSystem | undefined>(
    system.solarSystems.find((s) => s.id === selectedElement)
  );

  const [data, setData] = useState<Matrix<CellBase>>([
    selectedSystem
      ? selectedSystem.radiationArray.map((s) => ({ value: s }))
      : [],
    selectedSystem
      ? selectedSystem.temperatureArray.map((s) => ({ value: s }))
      : [],
  ]);

  const [tableMode, setTableMode] = useState('view');

  const [columnLabels, setColumnLabels] = useState(
    selectedSystem
      ? selectedSystem.radiationArray.map((s, index) => `P ${index + 1}`)
      : []
  );

  useEffect(() => {
    setSelectedSystem(() => {
      const newSystem = system.solarSystems.find(
        (s) => s.id === selectedElement
      );
      if (newSystem) {
        setData([
          newSystem.radiationArray.map((s) => ({ value: s })),
          newSystem.temperatureArray.map((s) => ({ value: s })),
        ]);
        setColumnLabels(
          newSystem.radiationArray.map((s, index) => `P ${index + 1}`)
        );
      }
      return newSystem;
    });
  }, [selectedElement, system]);

  const handleSelectedSystem = (e: any) => {
    setSelectedElement(e.target.value);
  };

  const handleTableOnBlur = () => {
    if (selectedSystem) {
      handleTableChange(data, selectedSystem.id, SmartSystemType.Solar);
    }
  };

  const handleTableOnChange = (e: any) => {
    if (tableMode === 'view') {
      setData(e);
    }
  };

  const handleOnKeyDown = (e: React.KeyboardEvent<Element>) => {
    if (!(e.ctrlKey === true && (e.key === 'v' || e.key === 'c'))) {
      e.preventDefault();
    }
  };

  const handleChange = (e: any) => {
    if (selectedSystem) {
      handleSystemChange(e, selectedSystem.id, SmartSystemType.Solar);
    }
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={12} xl={12}>
        <FormControl fullWidth>
          <InputLabel id="solar-system">Sistema solar</InputLabel>
          <Select
            labelId="solar-system"
            label="Sistema solar"
            value={selectedElement}
            onChange={handleSelectedSystem}
          >
            {system.solarSystems.map((s, index) => {
              return (
                <MenuItem key={s.id} value={s.id}>
                  {`${index + 1}. ${s.name} (${getValueByKey(
                    SolarPanelModuleText,
                    s.moduleType
                  )})`}
                </MenuItem>
              );
            })}
          </Select>
        </FormControl>
      </Grid>
      {selectedSystem && (
        <>
          <Grid item xs={12} md={12} xl={6}>
            <h3>Parámetros simulación</h3>
            <Grid container spacing={2}>
              <Grid item xs={12} md={12} xl={12}>
                <FormControl fullWidth>
                  <TextField
                    label="Nombre"
                    value={selectedSystem.name}
                    name="name"
                    autoComplete="off"
                    onChange={handleChange}
                  />
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6} xl={6}>
                <CustomNumberField
                  variable={selectedSystem.modulesNumber}
                  name="modulesNumber"
                  isInteger={true}
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={6}>
                <CustomNumberField
                  variable={selectedSystem.modulePower}
                  name="modulePower"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={6}>
                <FormControl fullWidth>
                  <InputLabel id="meteorologicalInformationMode-type">
                    Modo de ingreso información meteorológica
                  </InputLabel>
                  <Select
                    labelId="meteorologicalInformationMode-type"
                    label="Modo de ingreso información meteorológica"
                    value={selectedSystem.meteorologicalInformationMode}
                    name="meteorologicalInformationMode"
                    onChange={handleChange}
                  >
                    {Object.keys(
                      ScenariosSolarPanelMeteorologicalInformationType
                    ).map((key) => {
                      if (
                        key ===
                          ScenariosSolarPanelMeteorologicalInformationType.Typical &&
                        system.steps.value !== 24
                      ) {
                        return null;
                      }
                      return (
                        <MenuItem key={key} value={key}>
                          {getValueByKey(
                            ScenariosSolarPanelMeteorologicalInformationText,
                            key
                          )}
                        </MenuItem>
                      );
                    })}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6} xl={6}>
                <FormControl fullWidth>
                  <InputLabel id="moduleType-type">Tipo de módulos</InputLabel>
                  <Select
                    labelId="moduleType-type"
                    label="Tipo de módulos"
                    value={selectedSystem.moduleType}
                    name="moduleType"
                    onChange={handleChange}
                  >
                    {Object.keys(SolarPanelModuleType).map((key) => (
                      <MenuItem key={key} value={key}>
                        {getValueByKey(SolarPanelModuleText, key)}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              {(selectedSystem.meteorologicalInformationMode ===
                ScenariosSolarPanelMeteorologicalInformationType.Fixed ||
                selectedSystem.meteorologicalInformationMode ===
                  ScenariosSolarPanelMeteorologicalInformationType.Typical) && (
                <>
                  <Grid item xs={12} md={6} xl={6}>
                    <CustomNumberField
                      variable={selectedSystem.radiation}
                      name="radiation"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={6} xl={6}>
                    <CustomNumberField
                      variable={selectedSystem.temperature}
                      name="temperature"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                </>
              )}
            </Grid>
          </Grid>
          <Grid item xs={12} md={12} xl={6}>
            <h3>Parámetros módulos solares</h3>
            <Grid container spacing={2}>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.deratingFactor}
                  name="deratingFactor"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.efficiency}
                  name="efficiency"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.nominalIrradiance}
                  name="nominalIrradiance"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.nominalTemperature}
                  name="nominalTemperature"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.testIrradiance}
                  name="testIrradiance"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.testTemperature}
                  name="testTemperature"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.operatingTemperature}
                  name="operatingTemperature"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.temperatureVariationCoefficient}
                  name="temperatureVariationCoefficient"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
            </Grid>
          </Grid>
          {selectedSystem.meteorologicalInformationMode ===
            ScenariosSolarPanelMeteorologicalInformationType.Custom && (
            <Grid item xs={12} md={12} xl={12}>
              <div style={{ maxWidth: '100%', overflow: 'auto' }}>
                <Spreadsheet
                  darkMode={userTheme === ThemeType.Dark}
                  data={data}
                  rowLabels={ROW_LABELS}
                  columnLabels={columnLabels}
                  onModeChange={setTableMode}
                  onBlur={handleTableOnBlur}
                  onChange={handleTableOnChange}
                  onKeyDown={handleOnKeyDown}
                />
              </div>
            </Grid>
          )}
        </>
      )}
    </Grid>
  );
};

export default SolarTab;
