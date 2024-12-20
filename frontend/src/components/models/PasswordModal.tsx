import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  InputAdornment,
  TextField,
} from '@mui/material';
import { useState } from 'react';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import { sha256 } from 'js-sha256';

type Props = {
  handleClose: (confirm: boolean, password: string | undefined) => void;
  open: boolean;
};

const PasswordModal = (props: Props) => {
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const { handleClose, open } = props;

  const handleClickShowPassword = () => setShowPassword(!showPassword);

  const handleModalClose = (confirm: boolean) => {
    setPassword('');
    setShowPassword(false);
    handleClose(confirm, confirm ? sha256(password) : undefined);
  };

  return (
    <Dialog open={open} onClose={() => handleModalClose(false)}>
      <DialogTitle>{'¿Activar modo entramiento?'}</DialogTitle>
      <DialogContent>
        <TextField
          label="Password"
          value={password}
          variant="outlined"
          type={showPassword ? 'text' : 'password'}
          onChange={(e) => setPassword(e.target.value)}
          sx={{ marginTop: '10px' }}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton onClick={handleClickShowPassword}>
                  {showPassword ? <VisibilityIcon /> : <VisibilityOffIcon />}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
      </DialogContent>
      <DialogActions>
        <Button
          variant="contained"
          color="error"
          onClick={() => handleModalClose(false)}
        >
          Cancelar
        </Button>
        <Button
          variant="contained"
          color="success"
          onClick={() => handleModalClose(true)}
          autoFocus
        >
          Confirmar
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default PasswordModal;
