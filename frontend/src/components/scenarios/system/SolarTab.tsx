import React, { useEffect, useRef, useState } from 'react';
import {
  ScenariosSolarPanelMeteorologicalInformationText,
  ScenariosSolarPanelMeteorologicalInformationType,
  SmartSystemType,
  SolarPanel,
  SolarPanelModuleText,
  SolarPanelModuleType,
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
import { SmartCityParameters } from '../../../types/scenarios/smartCity';

type Props = {
  system: SmartCityParameters;
  handleSystemChange: (e: any, id: string, type: SmartSystemType) => void;
  handleTableChange: (
    e: Matrix<{
      value: number;
    }>,
    id: string,
    type: SmartSystemType
  ) => void;
};

const ROW_LABELS: string[] = ['Radiación [W / m²]', 'Temperatura [°C]'];

const SolarTab = (props: Props) => {
  const { system, handleSystemChange, handleTableChange } = props;

  const userTheme = useAppSelector((state) => state.theme.value);

  const table = useRef<any>();

  const [selectedElement, setSelectedElement] = useState<string | undefined>(
    system.solarPanels.length > 0 ? system.solarPanels[0].id : undefined
  );

  const [selectedSystem, setSelectedSystem] = useState<SolarPanel | undefined>(
    system.solarPanels.find((s) => s.id === selectedElement)
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
      const newSystem = system.solarPanels.find(
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
            {system.solarPanels.map((sP, index) => {
              return (
                <MenuItem key={sP.id} value={sP.id}>
                  {`${index + 1}. ${sP.name} (${getValueByKey(
                    SolarPanelModuleText,
                    sP.moduleType
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
                    onChange={(e: any) =>
                      handleSystemChange(
                        e,
                        selectedSystem.id,
                        SmartSystemType.Solar
                      )
                    }
                  />
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6} xl={6}>
                <CustomNumberField
                  variable={selectedSystem.modulesNumber}
                  name="modulesNumber"
                  isInteger={true}
                  handleChange={(e: any) =>
                    handleSystemChange(
                      e,
                      selectedSystem.id,
                      SmartSystemType.Solar
                    )
                  }
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={6} xl={6}>
                <CustomNumberField
                  variable={selectedSystem.modulePower}
                  name="modulePower"
                  handleChange={(e: any) =>
                    handleSystemChange(
                      e,
                      selectedSystem.id,
                      SmartSystemType.Solar
                    )
                  }
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
                    onChange={(e: any) =>
                      handleSystemChange(
                        e,
                        selectedSystem.id,
                        SmartSystemType.Solar
                      )
                    }
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
                    onChange={(e: any) =>
                      handleSystemChange(
                        e,
                        selectedSystem.id,
                        SmartSystemType.Solar
                      )
                    }
                  >
                    {Object.keys(SolarPanelModuleType).map((key) => (
                      <MenuItem key={key} value={key}>
                        {getValueByKey(SolarPanelModuleText, key)}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              {selectedSystem.meteorologicalInformationMode ===
                ScenariosSolarPanelMeteorologicalInformationType.Fixed && (
                <>
                  <Grid item xs={12} md={6} xl={6}>
                    <CustomNumberField
                      variable={selectedSystem.radiation}
                      name="radiation"
                      handleChange={(e: any) =>
                        handleSystemChange(
                          e,
                          selectedSystem.id,
                          SmartSystemType.Solar
                        )
                      }
                    ></CustomNumberField>
                  </Grid>
                  <Grid item xs={12} md={6} xl={6}>
                    <CustomNumberField
                      variable={selectedSystem.temperature}
                      name="temperature"
                      handleChange={(e: any) =>
                        handleSystemChange(
                          e,
                          selectedSystem.id,
                          SmartSystemType.Solar
                        )
                      }
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
                  handleChange={(e: any) =>
                    handleSystemChange(
                      e,
                      selectedSystem.id,
                      SmartSystemType.Solar
                    )
                  }
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.efficiency}
                  name="efficiency"
                  handleChange={(e: any) =>
                    handleSystemChange(
                      e,
                      selectedSystem.id,
                      SmartSystemType.Solar
                    )
                  }
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.nominalIrradiance}
                  name="nominalIrradiance"
                  handleChange={(e: any) =>
                    handleSystemChange(
                      e,
                      selectedSystem.id,
                      SmartSystemType.Solar
                    )
                  }
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.nominalTemperature}
                  name="nominalTemperature"
                  handleChange={(e: any) =>
                    handleSystemChange(
                      e,
                      selectedSystem.id,
                      SmartSystemType.Solar
                    )
                  }
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.testIrradiance}
                  name="testIrradiance"
                  handleChange={(e: any) =>
                    handleSystemChange(
                      e,
                      selectedSystem.id,
                      SmartSystemType.Solar
                    )
                  }
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.testTemperature}
                  name="testTemperature"
                  handleChange={(e: any) =>
                    handleSystemChange(
                      e,
                      selectedSystem.id,
                      SmartSystemType.Solar
                    )
                  }
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.operatingTemperature}
                  name="operatingTemperature"
                  handleChange={(e: any) =>
                    handleSystemChange(
                      e,
                      selectedSystem.id,
                      SmartSystemType.Solar
                    )
                  }
                ></CustomNumberField>
              </Grid>
              <Grid item xs={12} md={12} xl={4}>
                <CustomNumberField
                  variable={selectedSystem.temperatureVariationCoefficient}
                  name="temperatureVariationCoefficient"
                  handleChange={(e: any) =>
                    handleSystemChange(
                      e,
                      selectedSystem.id,
                      SmartSystemType.Solar
                    )
                  }
                ></CustomNumberField>
              </Grid>
            </Grid>
          </Grid>
          {selectedSystem.meteorologicalInformationMode ===
            ScenariosSolarPanelMeteorologicalInformationType.Custom && (
            <Grid item xs={12} md={12} xl={12}>
              <div style={{ maxWidth: '100%', overflow: 'auto' }} ref={table}>
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
