import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from '@mui/material';
import React from 'react';
import { setError } from '../../redux/slices/errorSlice';
import { useAppDispatch, useAppSelector } from '../../redux/reduxHooks';

const ErrorDialog = () => {
  const dispatch = useAppDispatch();
  const error = useAppSelector((state) => state.error);

  const closeErrorDialog = () => {
    dispatch(setError({ isShown: false, message: '' }));
  };

  return (
    <React.Fragment>
      <Dialog
        open={error.isShown}
        onClose={closeErrorDialog}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{'Algo salió mal'}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            {error.message}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeErrorDialog} variant="contained" color="error">
            Cerrar
          </Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
};

export default ErrorDialog;
