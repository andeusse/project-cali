import {
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from '@mui/material';
import React, { useEffect, useState } from 'react';
import {
  BatterySystem,
  BatteryText,
  BatteryType,
  ScenariosBatteryInformationText,
  ScenariosBatteryInformationType,
  SmartSystemType,
  TabProps,
} from '../../../types/scenarios/common';
import Spreadsheet, { Matrix, CellBase } from 'react-spreadsheet';
import { useAppSelector } from '../../../redux/reduxHooks';
import { getValueByKey } from '../../../utils/getValueByKey';
import CustomNumberField from '../../UI/CustomNumberField';
import { ThemeType } from '../../../types/theme';

const ROW_LABELS: string[] = [
  'Potencia de carga [kW]',
  'Potencia de descarga [kW]',
];

const BatteryTab = (props: TabProps) => {
  const { system, handleSystemChange, handleTableChange } = props;

  const userTheme = useAppSelector((state) => state.theme.value);

  const [selectedElement, setSelectedElement] = useState<string | undefined>(
    system.batterySystems.length > 0 ? system.batterySystems[0].id : undefined
  );

  const [selectedSystem, setSelectedSystem] = useState<
    BatterySystem | undefined
  >(system.batterySystems.find((s) => s.id === selectedElement));

  const [data, setData] = useState<Matrix<CellBase>>([
    selectedSystem
      ? selectedSystem.chargePowerArray.map((s) => ({ value: s }))
      : [],
    selectedSystem
      ? selectedSystem.dischargePowerArray.map((s) => ({ value: s }))
      : [],
  ]);

  const [tableMode, setTableMode] = useState('view');

  const [columnLabels, setColumnLabels] = useState(
    selectedSystem
      ? selectedSystem.chargePowerArray.map((s, index) => `P ${index + 1}`)
      : []
  );

  useEffect(() => {
    setSelectedSystem(() => {
      const newSystem = system.batterySystems.find(
        (s) => s.id === selectedElement
      );
      if (newSystem) {
        setData([
          newSystem.chargePowerArray.map((s) => ({ value: s })),
          newSystem.chargePowerArray.map((s) => ({ value: s })),
        ]);
        setColumnLabels(
          newSystem.chargePowerArray.map((s, index) => `P ${index + 1}`)
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
      handleTableChange(data, selectedSystem.id, SmartSystemType.Battery);
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
      handleSystemChange(e, selectedSystem.id, SmartSystemType.Battery);
    }
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={12} xl={12}>
        <FormControl fullWidth>
          <InputLabel id="battery-system">Sistema de batería</InputLabel>
          <Select
            labelId="battery-system"
            label="Sistema de batería"
            value={selectedElement}
            onChange={handleSelectedSystem}
          >
            {system.batterySystems.map((s, index) => {
              return (
                <MenuItem key={s.id} value={s.id}>
                  {`${index + 1}. ${s.name} (${getValueByKey(
                    BatteryText,
                    s.batteryType
                  )})`}
                </MenuItem>
              );
            })}
          </Select>
        </FormControl>
      </Grid>
      {selectedSystem && (
        <>
          <Grid item xs={12} md={12} xl={9}>
            <h3>Parámetros simulación</h3>
            <Grid container spacing={2}>
              <Grid item xs={12} md={12} xl={4}>
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
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.storageCapacity}
                  name="storageCapacity"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.maxChargePower}
                  name="maxChargePower"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.minChargePower}
                  name="minChargePower"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.maxDischargePower}
                  name="maxDischargePower"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.minDischargePower}
                  name="minDischargePower"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.stateOfCharge}
                  name="stateOfCharge"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <FormControl fullWidth>
                  <InputLabel id="batteryType-type">Tipo de batería</InputLabel>
                  <Select
                    labelId="batteryType-type"
                    label="Tipo de batería"
                    value={selectedSystem.batteryType}
                    name="batteryType"
                    onChange={handleChange}
                  >
                    {Object.keys(BatteryType).map((key) => (
                      <MenuItem key={key} value={key}>
                        {getValueByKey(BatteryText, key)}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <FormControl fullWidth>
                  <InputLabel id="informationMode-type">
                    Modo ingreso de información
                  </InputLabel>
                  <Select
                    labelId="informationMode-type"
                    label="Modo ingreso de información"
                    value={selectedSystem.informationMode}
                    name="informationMode"
                    onChange={handleChange}
                  >
                    {Object.keys(ScenariosBatteryInformationType).map((key) => (
                      <MenuItem key={key} value={key}>
                        {getValueByKey(ScenariosBatteryInformationText, key)}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={12} md={12} xl={3}>
            <h3>Parámetros baterías</h3>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6} xl={12}>
                <CustomNumberField
                  variable={selectedSystem.selfDischargeCoefficient}
                  name="selfDischargeCoefficient"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={12}>
                <CustomNumberField
                  variable={selectedSystem.chargeEfficiency}
                  name="chargeEfficiency"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={12}>
                <CustomNumberField
                  variable={selectedSystem.dischargeDischargeEfficiency}
                  name="dischargeDischargeEfficiency"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
            </Grid>
          </Grid>
          {selectedSystem.informationMode ===
            ScenariosBatteryInformationType.Custom && (
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

export default BatteryTab;
