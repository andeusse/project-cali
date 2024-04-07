import { FormControlLabel, Switch } from '@mui/material';

type Props = {
  name: string;
  value: boolean;
  handleChange: (e: any) => void;
  falseString?: string;
  trueString?: string;
  disabled?: boolean;
};

const CustomToggle = (props: Props) => {
  const { name, value, handleChange, falseString, trueString, disabled } =
    props;

  return (
    <FormControlLabel
      control={
        <Switch
          checked={value}
          name={name}
          onChange={(e: any) => handleChange(e)}
          color="default"
          disabled={disabled}
        />
      }
      label={
        value
          ? trueString
            ? trueString
            : 'Manual'
          : falseString
          ? falseString
          : 'Auto'
      }
    />
  );
};

export default CustomToggle;
