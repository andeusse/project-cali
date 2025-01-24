import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from '@mui/material';
import React from 'react';

type Props = {
  handleClose: (confirm: boolean) => void;
  open: boolean;
};

const ConfimationModal = (props: Props) => {
  const { handleClose, open } = props;

  const handleModalClose = (confirm: boolean) => {
    handleClose(confirm);
  };

  return (
    <Dialog open={open} onClose={() => handleModalClose(false)}>
      <DialogTitle>{'¿Desea desactivar el modo entrenamiento?'}</DialogTitle>
      <DialogContent></DialogContent>
      <DialogActions>
        <Button
          variant="contained"
          color="error"
          onClick={() => handleModalClose(false)}
        >
          No
        </Button>
        <Button
          variant="contained"
          color="success"
          onClick={() => handleModalClose(true)}
          autoFocus
        >
          Si
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ConfimationModal;
