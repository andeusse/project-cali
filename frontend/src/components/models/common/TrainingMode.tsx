import { Grid } from '@mui/material';
import { useState } from 'react';
import ConfimationModal from '../../UI/ConfimationModal';
import CustomToggle from '../../UI/CustomToggle';
import PasswordModal from '../PasswordModal';
import { modelsAPI } from '../../../api/digitalTwinsModels';
import { errorResp, loginInput, loginOutput } from '../../../types/api';
import { useAppDispatch } from '../../../redux/reduxHooks';
import { setError } from '../../../redux/slices/errorSlice';
import { AxiosError } from 'axios';
import Constants from '../../../config/constants';
import { setFormState } from '../../../utils/setFormState';
import { digitalTwinsType } from '../../../types/digitalTwinsType';

type Props<T> = {
  isPlaying: boolean;
  system: T;
  setSystem: React.Dispatch<React.SetStateAction<T>>;
};

const TrainingMode = <T extends digitalTwinsType>(props: Props<T>) => {
  const { isPlaying, system, setSystem } = props;
  const dispatch = useAppDispatch();

  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [showConfimationModal, setShowConfimationModal] = useState(false);
  const [passwordEl, setPasswordEl] = useState<any>(undefined);

  const handleTrainingModeChange = (e: any) => {
    setPasswordEl({
      target: {
        type: 'checkbox',
        checked: e.target.checked,
        name: e.target.name,
      },
    });
    if (e.target.checked) {
      setShowPasswordModal(true);
    } else {
      setShowConfimationModal(true);
    }
  };

  const handlePasswordModalClose = (
    confirm: boolean,
    password: string | undefined
  ) => {
    if (confirm && password !== undefined) {
      modelsAPI<loginOutput, loginInput>('trainingMode', {
        password: password,
      })
        .then((resp) => {
          if (resp.data.succeed) {
            const newState = setFormState<T>(passwordEl, system);
            if (newState) {
              setSystem(newState as T);
            }
          } else {
            dispatch(
              setError({
                isShown: true,
                message: Constants.WRONG_PASSWORD,
              })
            );
          }
        })
        .catch((err: AxiosError<errorResp>) => {
          dispatch(
            setError({
              isShown: true,
              message: err.message,
            })
          );
        })
        .finally(() => {});
    }
    setShowPasswordModal(false);
  };

  const handleConfirmationModalClose = (confirm: boolean) => {
    if (confirm) {
      const newState = setFormState<T>(passwordEl, system);
      if (newState) {
        setSystem(newState as T);
      }
    }
    setShowConfimationModal(false);
  };

  return (
    <Grid container>
      <PasswordModal
        handleClose={handlePasswordModalClose}
        open={showPasswordModal}
      ></PasswordModal>
      <ConfimationModal
        open={showConfimationModal}
        handleClose={handleConfirmationModalClose}
      ></ConfimationModal>
      <Grid item xs={12} md={7} xl={7}>
        <h3>Entrenamiento</h3>
      </Grid>
      <Grid
        item
        xs={12}
        md={5}
        xl={5}
        alignContent={'center'}
        sx={{ paddingLeft: '16px' }}
      >
        <CustomToggle
          name="trainingMode"
          value={system.trainingMode}
          handleChange={handleTrainingModeChange}
          trueString="On"
          falseString="Off"
          disabled={isPlaying}
        ></CustomToggle>
      </Grid>
    </Grid>
  );
};

export default TrainingMode;
