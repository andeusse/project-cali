import AtomicSpinner from 'atomic-spinner';
import CSS from 'csstype';

type Props = {
  isLoading: boolean;
};

const IsLoading = (props: Props) => {
  const { isLoading } = props;
  return (
    <>
      {isLoading && (
        <>
          <div style={backGroundStyle}></div>
          <div style={loadingStyle}>
            <AtomicSpinner atomSize={400}></AtomicSpinner>
          </div>
        </>
      )}
    </>
  );
};

export default IsLoading;

const loadingStyle: CSS.Properties = {
  position: 'fixed',
  top: '50%',
  left: '50%',
  marginTop: '-200px',
  marginLeft: '-200px',
  width: '400px',
  height: '400px',
};

const backGroundStyle: CSS.Properties = {
  position: 'fixed',
  width: '100%',
  height: '100%',
  backgroundColor: 'rgba(200,200,200,0.2)',
  zIndex: 999,
};
