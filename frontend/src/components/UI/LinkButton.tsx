import { Button, ButtonProps } from '@mui/material';
import { FunctionComponent } from 'react';
import { Link as RouterLink } from 'react-router-dom';

type Props = {
  to: string;
};

const LinkButton: FunctionComponent<Props & ButtonProps> = (props) => {
  return <Button {...props}>{props.children}</Button>;
};

LinkButton.defaultProps = {
  variant: 'text',
  color: 'primary',
  component: RouterLink,
};

export default LinkButton;
