import React, { useState } from 'react';
import Button from '@mui/material/Button';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import StopIcon from '@mui/icons-material/Stop';

type PlayerControlsProps = {
  onPlay: () => void;
  onPause: () => void;
  onStop: () => void;
};

const PlayerControls: React.FC<PlayerControlsProps> = ({
  onPlay,
  onPause,
  onStop,
}) => {
  const [isPlaying, setIsPlaying] = useState(false);

  const handlePlay = () => {
    setIsPlaying(true);
    onPlay();
  };

  const handlePause = () => {
    setIsPlaying(false);
    onPause();
  };

  const handleStop = () => {
    setIsPlaying(false);
    onStop();
  };

  return (
    <div>
      <Button
        variant="contained"
        onClick={handlePlay}
        disabled={isPlaying}
        startIcon={<PlayArrowIcon />}
      >
        Play
      </Button>
      <Button
        variant="contained"
        onClick={handlePause}
        disabled={!isPlaying}
        startIcon={<PauseIcon />}
      >
        Pause
      </Button>
      <Button
        variant="contained"
        onClick={handleStop}
        disabled={!isPlaying}
        startIcon={<StopIcon />}
      >
        Stop
      </Button>
    </div>
  );
};

export default PlayerControls;
