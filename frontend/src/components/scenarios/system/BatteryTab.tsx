import {
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from '@mui/material';
import React, { useCallback, useEffect, useState } from 'react';
import {
  BatterySystem,
  BatteryText,
  BatteryType,
  ScenariosCommonInputInformationText,
  ScenariosCommonInputInformationType,
  SmartSystemType,
  TabProps,
} from '../../../types/scenarios/common';
import { useAppSelector } from '../../../redux/reduxHooks';
import { getValueByKey } from '../../../utils/getValueByKey';
import CustomNumberField from '../../UI/CustomNumberField';
import { ThemeType } from '../../../types/theme';
import {
  CellChange,
  Column,
  DefaultCellTypes,
  ReactGrid,
  Row,
} from '@silevis/reactgrid';

const BatteryTab = (props: TabProps) => {
  const { system, handleSystemChange, handleTableChange } = props;

  const userTheme = useAppSelector((state) => state.theme.value);

  const [selectedElement, setSelectedElement] = useState<string | undefined>(
    system.batterySystems.length > 0 ? system.batterySystems[0].id : undefined
  );

  const [selectedSystem, setSelectedSystem] = useState<
    BatterySystem | undefined
  >(system.batterySystems.find((s) => s.id === selectedElement));

  const getColumns = useCallback((): Column[] => {
    if (selectedSystem) {
      let arr: Column[] = [
        { columnId: `variables`, width: 200 },
        ...selectedSystem.chargePowerArray.map((v, i) => {
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
          ...selectedSystem.chargePowerArray.map((v, i) => {
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
          { type: 'header', text: 'Potencia de carga [kW]', nonEditable: true },
          ...selectedSystem.chargePowerArray.map((v, i) => {
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
          {
            type: 'header',
            text: 'Potencia de descarga [kW]',
            nonEditable: true,
          },
          ...selectedSystem.dischargePowerArray.map((v, i) => {
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
      const newSystem = system.batterySystems.find(
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
      handleTableChange(e, selectedSystem.id, SmartSystemType.Battery);
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
                    {Object.keys(ScenariosCommonInputInformationType).map(
                      (key) => (
                        <MenuItem key={key} value={key}>
                          {getValueByKey(
                            ScenariosCommonInputInformationText,
                            key
                          )}
                        </MenuItem>
                      )
                    )}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <FormControl fullWidth>
                  <InputLabel id="type-type">Tipo de batería</InputLabel>
                  <Select
                    labelId="type-type"
                    label="Tipo de batería"
                    value={selectedSystem.type}
                    name="type"
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
                  variable={selectedSystem.dischargeEfficiency}
                  name="dischargeEfficiency"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
            </Grid>
          </Grid>
          {selectedSystem.informationMode ===
            ScenariosCommonInputInformationType.Custom && (
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

export default BatteryTab;
