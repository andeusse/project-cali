import Iframe from 'react-iframe';

type Props = {
  url: string;
};

const IframeFull = (props: Props) => {
  const { url } = props;
  return (
    <Iframe
      url={url}
      styles={{
        position: 'absolute',
        width: '100%',
        height: '100%',
        left: 0,
        right: 0,
      }}
    ></Iframe>
  );
};

export default IframeFull;
