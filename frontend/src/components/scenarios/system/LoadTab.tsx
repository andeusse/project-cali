import React, { useCallback, useEffect, useState } from 'react';
import {
  LoadSystem,
  ScenariosLoadInputInformationText,
  ScenariosLoadInputInformationType,
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

const LoadTab = (props: TabProps) => {
  const { system, handleSystemChange, handleTableChange } = props;

  const userTheme = useAppSelector((state) => state.theme.value);

  const [selectedElement, setSelectedElement] = useState<string | undefined>(
    system.loadSystems.length > 0 ? system.loadSystems[0].id : undefined
  );

  const [selectedSystem, setSelectedSystem] = useState<LoadSystem | undefined>(
    system.loadSystems.find((s) => s.id === selectedElement)
  );

  const getColumns = useCallback((): Column[] => {
    if (selectedSystem) {
      let arr: Column[] = [
        { columnId: `variables`, width: 200 },
        ...selectedSystem.powerArray.map((v, i) => {
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
          ...selectedSystem.powerArray.map((v, i) => {
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
            text: 'Potencia de demanda [kW]',
            nonEditable: true,
          },
          ...selectedSystem.powerArray.map((v, i) => {
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
      const newSystem = system.loadSystems.find(
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
      handleTableChange(e, selectedSystem.id, SmartSystemType.Load);
    }
  };

  const handleChange = (e: any) => {
    if (selectedSystem) {
      handleSystemChange(e, selectedSystem.id, SmartSystemType.Load);
    }
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={12} xl={12}>
        <FormControl fullWidth>
          <InputLabel id="load-system">Carga</InputLabel>
          <Select
            labelId="load-system"
            label="Carga"
            value={selectedElement}
            onChange={handleSelectedSystem}
          >
            {system.loadSystems.map((s, index) => {
              return (
                <MenuItem key={s.id} value={s.id}>
                  {`${index + 1}. ${s.name}`}
                </MenuItem>
              );
            })}
          </Select>
        </FormControl>
      </Grid>
      {selectedSystem && (
        <>
          <Grid item xs={12} md={12} xl={12}>
            <h3>Parámetros simulación</h3>
            <Grid container spacing={2}>
              <Grid item xs={12} md={12} xl={3}>
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
              <Grid item xs={12} md={12} xl={3}>
                <FormControl fullWidth>
                  <InputLabel id="load-type">Tipo de carga</InputLabel>
                  <Select
                    labelId="load-type"
                    label="Tipo de carga"
                    value={selectedSystem.informationMode}
                    name="informationMode"
                    onChange={handleChange}
                  >
                    {Object.keys(ScenariosLoadInputInformationType).map(
                      (key) => {
                        if (
                          (key ===
                            ScenariosLoadInputInformationType.Industrial ||
                            key ===
                              ScenariosLoadInputInformationType.Commercial ||
                            key ===
                              ScenariosLoadInputInformationType.Residential) &&
                          system.steps.value !== 24
                        ) {
                          return null;
                        }
                        return (
                          <MenuItem key={key} value={key}>
                            {getValueByKey(
                              ScenariosLoadInputInformationText,
                              key
                            )}
                          </MenuItem>
                        );
                      }
                    )}
                  </Select>
                </FormControl>
              </Grid>
              {selectedSystem.informationMode ===
                ScenariosLoadInputInformationType.Fixed && (
                <Grid item xs={12} md={6} xl={3}>
                  <CustomNumberField
                    variable={selectedSystem.power}
                    name="power"
                    handleChange={handleChange}
                  ></CustomNumberField>
                </Grid>
              )}
              {(selectedSystem.informationMode ===
                ScenariosLoadInputInformationType.Industrial ||
                selectedSystem.informationMode ===
                  ScenariosLoadInputInformationType.Commercial ||
                selectedSystem.informationMode ===
                  ScenariosLoadInputInformationType.Residential) &&
                system.steps.value === 24 && (
                  <Grid item xs={12} md={6} xl={3}>
                    <CustomNumberField
                      variable={selectedSystem.peakPower}
                      name="peakPower"
                      handleChange={handleChange}
                    ></CustomNumberField>
                  </Grid>
                )}
            </Grid>
          </Grid>
          {selectedSystem.informationMode ===
            ScenariosLoadInputInformationType.Custom && (
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

export default LoadTab;
