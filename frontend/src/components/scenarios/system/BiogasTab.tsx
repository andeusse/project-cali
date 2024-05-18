import React, { useEffect, useState } from 'react';
import {
  BiogasSystem,
  BiogasText,
  BiogasType,
  SmartSystemType,
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
import { useAppSelector } from '../../../redux/reduxHooks';
import { getValueByKey } from '../../../utils/getValueByKey';
import CustomNumberField from '../../UI/CustomNumberField';

const BiogasTab = (props: TabProps) => {
  const { system, handleSystemChange, handleTableChange } = props;

  const userTheme = useAppSelector((state) => state.theme.value);

  const [selectedElement, setSelectedElement] = useState<string | undefined>(
    system.biogasSystems.length > 0 ? system.biogasSystems[0].id : undefined
  );

  const [selectedSystem, setSelectedSystem] = useState<
    BiogasSystem | undefined
  >(system.biogasSystems.find((s) => s.id === selectedElement));

  useEffect(() => {
    setSelectedSystem(() => {
      const newSystem = system.biogasSystems.find(
        (s) => s.id === selectedElement
      );
      return newSystem;
    });
  }, [selectedElement, system]);

  const handleSelectedSystem = (e: any) => {
    setSelectedElement(e.target.value);
  };

  const handleChange = (e: any) => {
    if (selectedSystem) {
      handleSystemChange(e, selectedSystem.id, SmartSystemType.Biogas);
    }
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={12} xl={12}>
        <FormControl fullWidth>
          <InputLabel id="biogas-system">Sistema biogas</InputLabel>
          <Select
            labelId="biogas-system"
            label="Sistema biogas"
            value={selectedElement}
            onChange={handleSelectedSystem}
          >
            {system.biogasSystems.map((s, index) => {
              return (
                <MenuItem key={s.id} value={s.id}>
                  {`${index + 1}. ${s.name} (${getValueByKey(
                    BiogasText,
                    s.type
                  )})`}
                </MenuItem>
              );
            })}
          </Select>
        </FormControl>
      </Grid>
      {selectedSystem && (
        <>
          <Grid item xs={12} md={12} xl={4}>
            <h3>Parámetros simulación</h3>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6} xl={12}>
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
                  variable={selectedSystem.stabilizationDays}
                  name="stabilizationDays"
                  isInteger={true}
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={6}>
                <CustomNumberField
                  variable={selectedSystem.ambientPressure}
                  name="ambientPressure"
                  isInteger={true}
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={6}>
                <CustomNumberField
                  variable={selectedSystem.ambienteTemperature}
                  name="ambienteTemperature"
                  isInteger={true}
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={6}>
                <CustomNumberField
                  variable={selectedSystem.electricGeneratorPower}
                  name="electricGeneratorPower"
                  isInteger={true}
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={6}>
                <CustomNumberField
                  variable={selectedSystem.electricGeneratorEfficiency}
                  name="electricGeneratorEfficiency"
                  isInteger={true}
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={6}>
                <FormControl fullWidth>
                  <InputLabel id="moduleType-type">Tipo de sistema</InputLabel>
                  <Select
                    labelId="moduleType-type"
                    label="Tipo de módulos"
                    value={selectedSystem.type}
                    name="type"
                    onChange={handleChange}
                  >
                    {Object.keys(BiogasType).map((key) => (
                      <MenuItem key={key} value={key}>
                        {getValueByKey(BiogasText, key)}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={12} md={12} xl={8}>
            <h3>Parámetros turbina eólica</h3>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.reactorVolume1}
                  name="reactorVolume1"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.reactorVolume2}
                  name="reactorVolume2"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.diameterHeightRatio1}
                  name="diameterHeightRatio1"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.diameterHeightRatio2}
                  name="diameterHeightRatio2"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.heatTransferCoefficient1}
                  name="heatTransferCoefficient1"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.heatTransferCoefficient2}
                  name="heatTransferCoefficient2"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.temperatureSetpoint1}
                  name="temperatureSetpoint1"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.temperatureSetpoint2}
                  name="temperatureSetpoint2"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.controllerTolerance1}
                  name="controllerTolerance1"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.controllerTolerance2}
                  name="controllerTolerance2"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.carbonConcentration}
                  name="carbonConcentration"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.hydrogenConcentration}
                  name="hydrogenConcentration"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.oxygenConcentration}
                  name="oxygenConcentration"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.sulfurConcentration}
                  name="sulfurConcentration"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.totalConcentration}
                  name="totalConcentration"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.substrateDensity}
                  name="substrateDensity"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.substrateTemperature}
                  name="substrateTemperature"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.substratePressure}
                  name="substratePressure"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.substrateFlow}
                  name="substrateFlow"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={3}>
                <CustomNumberField
                  variable={selectedSystem.substratePresurreDrop}
                  name="substratePresurreDrop"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
            </Grid>
          </Grid>
        </>
      )}
    </Grid>
  );
};

export default BiogasTab;
