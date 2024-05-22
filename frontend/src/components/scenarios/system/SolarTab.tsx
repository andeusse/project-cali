import React, { useCallback, useEffect, useState } from 'react';
import {
  ScenariosSolarWindInputInformationText,
  ScenariosSolarWindInputInformationType,
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
import CustomNumberField from '../../UI/CustomNumberField';
import { getValueByKey } from '../../../utils/getValueByKey';
import { useAppSelector } from '../../../redux/reduxHooks';
import { ThemeType } from '../../../types/theme';
import {
  ReactGrid,
  Column,
  Row,
  DefaultCellTypes,
  CellChange,
} from '@silevis/reactgrid';
import './table.scss';

const SolarTab = (props: TabProps) => {
  const { system, handleSystemChange, handleTableChange } = props;

  const userTheme = useAppSelector((state) => state.theme.value);

  const [selectedElement, setSelectedElement] = useState<string | undefined>(
    system.solarSystems.length > 0 ? system.solarSystems[0].id : undefined
  );

  const [selectedSystem, setSelectedSystem] = useState<SolarSystem | undefined>(
    system.solarSystems.find((s) => s.id === selectedElement)
  );

  const getColumns = useCallback((): Column[] => {
    if (selectedSystem) {
      let arr: Column[] = [
        { columnId: `variables`, width: 200 },
        ...selectedSystem.radiationArray.map((v, i) => {
          const col: Column = {
            columnId: `${i}`,
            width: 100,
          };
          return col;
        }),
      ];
      return arr;
    }
    return [];
  }, [selectedSystem]);

  const getRows = useCallback((): Row[] => {
    if (selectedSystem) {
      let arr: Row[] = [];
      arr.push({
        rowId: 'header',
        cells: [
          { type: 'header', text: '', nonEditable: true },
          ...selectedSystem.radiationArray.map((v, i) => {
            const col: DefaultCellTypes = {
              type: 'header',
              text: `P ${i + 1}`,
              nonEditable: true,
            };
            return col;
          }),
        ],
      });
      arr.push({
        rowId: '0',
        cells: [
          { type: 'header', text: 'Irradiancia [W / m²]', nonEditable: true },
          ...selectedSystem.radiationArray.map((v, i) => {
            const col: DefaultCellTypes = {
              type: 'number',
              value: v,
            };
            return col;
          }),
        ],
      });
      arr.push({
        rowId: '1',
        cells: [
          { type: 'header', text: 'Temperatura [°C]', nonEditable: true },
          ...selectedSystem.temperatureArray.map((v, i) => {
            const col: DefaultCellTypes = {
              type: 'number',
              value: v,
            };
            return col;
          }),
        ],
      });
      return arr;
    }
    return [];
  }, [selectedSystem]);

  const [rows, setRows] = useState<Row[]>(getRows());

  const [columns, setColumns] = useState<Column[]>(getColumns());

  useEffect(() => {
    setSelectedSystem(() => {
      const newSystem = system.solarSystems.find(
        (s) => s.id === selectedElement
      );
      if (newSystem) {
        setRows(getRows());
        setColumns(getColumns());
      }
      return newSystem;
    });
  }, [getColumns, getRows, selectedElement, system]);

  const handleSelectedSystem = (e: any) => {
    setSelectedElement(e.target.value);
  };

  const handleCellsChange = (e: CellChange[]) => {
    if (selectedSystem) {
      handleTableChange(e, selectedSystem.id, SmartSystemType.Solar);
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
                  {`${s.name} (${getValueByKey(SolarPanelModuleText, s.type)})`}
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
                  <InputLabel id="informationMode-type">
                    Modo de ingreso información meteorológica
                  </InputLabel>
                  <Select
                    labelId="informationMode-type"
                    label="Modo de ingreso información meteorológica"
                    value={selectedSystem.informationMode}
                    name="informationMode"
                    onChange={handleChange}
                  >
                    {Object.keys(ScenariosSolarWindInputInformationType).map(
                      (key) => {
                        if (
                          key ===
                            ScenariosSolarWindInputInformationType.Typical &&
                          system.steps.value !== 24
                        ) {
                          return null;
                        }
                        return (
                          <MenuItem key={key} value={key}>
                            {getValueByKey(
                              ScenariosSolarWindInputInformationText,
                              key
                            )}
                          </MenuItem>
                        );
                      }
                    )}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6} xl={6}>
                <FormControl fullWidth>
                  <InputLabel id="moduleType-type">Tipo de módulos</InputLabel>
                  <Select
                    labelId="moduleType-type"
                    label="Tipo de módulos"
                    value={selectedSystem.type}
                    name="type"
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
              {(selectedSystem.informationMode ===
                ScenariosSolarWindInputInformationType.Fixed ||
                selectedSystem.informationMode ===
                  ScenariosSolarWindInputInformationType.Typical) && (
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
          {selectedSystem.informationMode ===
            ScenariosSolarWindInputInformationType.Custom && (
            <Grid item xs={12} md={12} xl={12}>
              <div
                id={
                  userTheme === ThemeType.Dark
                    ? 'reactgrid-dark-mode'
                    : 'reactgrid-light-mode'
                }
                style={{ maxWidth: '100%', overflow: 'auto' }}
              >
                <ReactGrid
                  rows={rows}
                  columns={columns}
                  onCellsChanged={(e: CellChange[]) => {
                    handleCellsChange(e);
                  }}
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
