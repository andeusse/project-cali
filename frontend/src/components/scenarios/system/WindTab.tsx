import {
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from '@mui/material';
import {
  Column,
  Row,
  DefaultCellTypes,
  CellChange,
  ReactGrid,
} from '@silevis/reactgrid';
import React, { useCallback, useEffect, useState } from 'react';
import { useAppSelector } from '../../../redux/reduxHooks';
import {
  ScenariosSolarWindInputInformationText,
  ScenariosSolarWindInputInformationType,
  SmartSystemType,
  TabProps,
  WindSystem,
  WindText,
  WindType,
} from '../../../types/scenarios/common';
import { getValueByKey } from '../../../utils/getValueByKey';
import CustomNumberField from '../../UI/CustomNumberField';
import { ThemeType } from '../../../types/theme';

const WindTab = (props: TabProps) => {
  const { system, handleSystemChange, handleTableChange } = props;

  const userTheme = useAppSelector((state) => state.theme.value);

  const [selectedElement, setSelectedElement] = useState<string | undefined>(
    system.windSystems.length > 0 ? system.windSystems[0].id : undefined
  );

  const [selectedSystem, setSelectedSystem] = useState<WindSystem | undefined>(
    system.windSystems.find((s) => s.id === selectedElement)
  );

  const getColumns = useCallback((): Column[] => {
    if (selectedSystem) {
      let arr: Column[] = [
        { columnId: `variables`, width: 200 },
        ...selectedSystem.windSpeedArray.map((v, i) => {
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
          ...selectedSystem.windSpeedArray.map((v, i) => {
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
          {
            type: 'header',
            text: 'Velocidad del viento [m / s]',
            nonEditable: true,
          },
          ...selectedSystem.windSpeedArray.map((v, i) => {
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
      const newSystem = system.windSystems.find(
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
      handleTableChange(e, selectedSystem.id, SmartSystemType.Wind);
    }
  };

  const handleChange = (e: any) => {
    if (selectedSystem) {
      handleSystemChange(e, selectedSystem.id, SmartSystemType.Wind);
    }
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={12} xl={12}>
        <FormControl fullWidth>
          <InputLabel id="wind-system">Sistema eólico</InputLabel>
          <Select
            labelId="wind-system"
            label="Sistema eólico"
            value={selectedElement}
            onChange={handleSelectedSystem}
          >
            {system.windSystems.map((s, index) => {
              return (
                <MenuItem key={s.id} value={s.id}>
                  {`${index + 1}. ${s.name} (${getValueByKey(
                    WindText,
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
          <Grid item xs={12} md={12} xl={6}>
            <h3>Parámetros simulación</h3>
            <Grid container spacing={2}>
              <Grid item xs={12} md={12} xl={8}>
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
                  variable={selectedSystem.turbineNumber}
                  name="turbineNumber"
                  isInteger={true}
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.nominalPower}
                  name="nominalPower"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
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
              <Grid item xs={12} md={6} xl={4}>
                <FormControl fullWidth>
                  <InputLabel id="moduleType-type">Tipo de módulos</InputLabel>
                  <Select
                    labelId="moduleType-type"
                    label="Tipo de módulos"
                    value={selectedSystem.type}
                    name="type"
                    onChange={handleChange}
                  >
                    {Object.keys(WindType).map((key) => (
                      <MenuItem key={key} value={key}>
                        {getValueByKey(WindText, key)}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={12} md={12} xl={6}>
            <h3>Parámetros turbina eólica</h3>
            <Grid container spacing={2}>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.rotorHeight}
                  name="rotorHeight"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.anemometerHeight}
                  name="anemometerHeight"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.ratedWindSpeed}
                  name="ratedWindSpeed"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.lowerCutoffWindSpeed}
                  name="lowerCutoffWindSpeed"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.upperCutoffWindSpeed}
                  name="upperCutoffWindSpeed"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.surfaceRoughnessLength}
                  name="surfaceRoughnessLength"
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

export default WindTab;
