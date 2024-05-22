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
  HydraulicSystem,
  ScenariosCommonInputInformationText,
  ScenariosCommonInputInformationType,
  SmartSystemType,
  TabProps,
  HydraulicText,
  HydraulicType,
} from '../../../types/scenarios/common';
import {
  Column,
  Row,
  DefaultCellTypes,
  CellChange,
  ReactGrid,
} from '@silevis/reactgrid';
import { useAppSelector } from '../../../redux/reduxHooks';
import { getValueByKey } from '../../../utils/getValueByKey';
import CustomNumberField from '../../UI/CustomNumberField';
import { ThemeType } from '../../../types/theme';

const HydraulicTab = (props: TabProps) => {
  const { system, handleSystemChange, handleTableChange } = props;

  const userTheme = useAppSelector((state) => state.theme.value);

  const [selectedElement, setSelectedElement] = useState<string | undefined>(
    system.hydraulicSystems.length > 0
      ? system.hydraulicSystems[0].id
      : undefined
  );

  const [selectedSystem, setSelectedSystem] = useState<
    HydraulicSystem | undefined
  >(system.hydraulicSystems.find((s) => s.id === selectedElement));

  const getColumns = useCallback((): Column[] => {
    if (selectedSystem) {
      let arr: Column[] = [
        { columnId: `variables`, width: 200 },
        ...selectedSystem.waterHeadArray.map((v, i) => {
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
          ...selectedSystem.waterHeadArray.map((v, i) => {
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
          { type: 'header', text: 'Cabeza de agua [m]', nonEditable: true },
          ...selectedSystem.waterHeadArray.map((v, i) => {
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
          { type: 'header', text: 'Flujo de agua [m³ / s]', nonEditable: true },
          ...selectedSystem.waterFlowArray.map((v, i) => {
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
      const newSystem = system.hydraulicSystems.find(
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
      handleTableChange(e, selectedSystem.id, SmartSystemType.Hydraulic);
    }
  };

  const handleChange = (e: any) => {
    if (selectedSystem) {
      handleSystemChange(e, selectedSystem.id, SmartSystemType.Hydraulic);
    }
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={12} xl={12}>
        <FormControl fullWidth>
          <InputLabel id="turbine-system">Sistema de turbinas</InputLabel>
          <Select
            labelId="turbine-system"
            label="Sistema de turbinas"
            value={selectedElement}
            onChange={handleSelectedSystem}
          >
            {system.hydraulicSystems.map((s, index) => {
              return (
                <MenuItem key={s.id} value={s.id}>
                  {`${s.name} (${getValueByKey(HydraulicText, s.type)})`}
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
                    Modo de ingreso información
                  </InputLabel>
                  <Select
                    labelId="informationMode-type"
                    label="Modo de ingreso información"
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
                  <InputLabel id="informationMode-type">
                    Modo de ingreso información
                  </InputLabel>
                  <Select
                    labelId="informationMode-type"
                    label="Modo de ingreso información"
                    value={selectedSystem.type}
                    name="type"
                    onChange={handleChange}
                  >
                    {Object.keys(HydraulicType).map((key) => (
                      <MenuItem key={key} value={key}>
                        {getValueByKey(HydraulicText, key)}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              {selectedSystem.informationMode ===
                ScenariosCommonInputInformationType.Fixed && (
                <>
                  <Grid item xs={12} md={6} xl={4}>
                    <CustomNumberField
                      variable={selectedSystem.waterHead}
                      name="waterHead"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={6} xl={4}>
                    <CustomNumberField
                      variable={selectedSystem.waterFlow}
                      name="waterFlow"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                </>
              )}
            </Grid>
          </Grid>
          <Grid item xs={12} md={12} xl={6}>
            <h3>Parámetros turbinas</h3>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.efficiency}
                  name="efficiency"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.frictionLosses}
                  name="frictionLosses"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.minimumWaterHead}
                  name="minimumWaterHead"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.maximumWaterHead}
                  name="maximumWaterHead"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.minimumWaterFlow}
                  name="minimumWaterFlow"
                  handleChange={handleChange}
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.maximumWaterFlow}
                  name="maximumWaterFlow"
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

export default HydraulicTab;
