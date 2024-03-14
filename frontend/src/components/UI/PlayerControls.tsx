import React, { useState } from 'react';
import Button from '@mui/material/Button';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import StopIcon from '@mui/icons-material/Stop';

type PlayerControlsProps = {
  isPlaying: boolean;
  onPlay: () => void;
  onPause: () => void;
  onStop: () => void;
};

const PlayerControls: React.FC<PlayerControlsProps> = ({
  isPlaying,
  onPlay,
  onPause,
  onStop,
}) => {
  const handlePlay = () => {
    onPlay();
  };

  const handlePause = () => {
    onPause();
  };

  const handleStop = () => {
    onStop();
  };

  return (
    <div
      style={{ textAlign: 'center', marginTop: '20px', marginBottom: '20px' }}
    >
      <Button
        variant="contained"
        onClick={handlePlay}
        disabled={isPlaying}
        startIcon={<PlayArrowIcon />}
        sx={{ width: '120px', margin: '5px' }}
      >
        Iniciar
      </Button>
      <Button
        variant="contained"
        onClick={handlePause}
        disabled={!isPlaying}
        startIcon={<PauseIcon />}
        sx={{ width: '120px', margin: '5px' }}
      >
        Pausar
      </Button>
      <Button
        variant="contained"
        onClick={handleStop}
        disabled={!isPlaying}
        startIcon={<StopIcon />}
        sx={{ width: '120px', margin: '5px' }}
      >
        Detener
      </Button>
    </div>
  );
};

export default PlayerControls;
