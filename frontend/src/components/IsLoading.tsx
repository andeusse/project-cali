import AtomicSpinner from 'atomic-spinner';
import CSS from 'csstype';

type Props = {
  isLoading: boolean;
};

const IsLoading = (props: Props) => {
  const { isLoading } = props;
  return (
    <div style={loadingStyle}>
      {isLoading && <AtomicSpinner></AtomicSpinner>}
    </div>
  );
};

export default IsLoading;

const loadingStyle: CSS.Properties = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  marginTop: '-100px',
  marginLeft: '-100px',
  width: '100px',
  height: '100px',
};
